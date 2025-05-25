"""Tiny HTTP server exposing the Lego GPT API via an RQ queue."""

import json
import os
import time
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from redis import Redis
from rq import Queue, Job
from backend.api import health
from backend import STATIC_ROOT, SUBMISSIONS_ROOT, COMMENTS_ROOT, HISTORY_ROOT
from backend.worker import QUEUE_NAME as DEFAULT_QUEUE, generate_job, detect_job
from backend.auth import decode as decode_jwt
from backend import __version__
from backend.logging_config import setup_logging
from urllib.request import urlopen
from urllib.parse import urlsplit, parse_qs


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_conn = Redis.from_url(REDIS_URL)
QUEUE_NAME = os.getenv("QUEUE_NAME", DEFAULT_QUEUE)
queue = Queue(QUEUE_NAME, connection=redis_conn)

JWT_SECRET = os.getenv("JWT_SECRET", "secret")
RATE_LIMIT = int(os.getenv("RATE_LIMIT", "5"))
# Allow cross-origin requests
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
# token -> (count, window_epoch_minute)
_TOKEN_USAGE: dict[str, tuple[int, int]] = {}

# Simple in-memory metrics
METRICS: dict[str, int] = {
    "generate_requests": 0,
    "detect_requests": 0,
    "example_submissions": 0,
}

# Base URLs of other Lego GPT instances for federated search
FEDERATED_INSTANCES = [u for u in os.getenv("FEDERATED_INSTANCES", "").split(",") if u]


def _local_examples() -> list[dict]:
    path = Path(__file__).resolve().parents[1] / "frontend/public/examples.json"
    try:
        return json.loads(path.read_text())
    except Exception:
        return []


def _fetch_examples(base: str) -> list[dict]:
    try:
        with urlopen(base.rstrip("/") + "/examples.json", timeout=3) as res:
            return json.loads(res.read().decode())
    except Exception:
        return []


def _check_auth(headers) -> None:
    auth = headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise PermissionError
    token = auth.split(" ", 1)[1]
    decode_jwt(token, JWT_SECRET)

    now = int(time.time())
    window = now // 60
    count, win = _TOKEN_USAGE.get(token, (0, window))
    if win != window:
        count = 0
        win = window
    if count >= RATE_LIMIT:
        raise RuntimeError("rate_limit")
    _TOKEN_USAGE[token] = (count + 1, win)


def _check_admin(headers) -> None:
    """Ensure JWT token has ``role`` set to ``admin``."""
    auth = headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise PermissionError
    token = auth.split(" ", 1)[1]
    payload = decode_jwt(token, JWT_SECRET)
    if payload.get("role") != "admin":
        raise PermissionError


class Handler(BaseHTTPRequestHandler):
    def _add_cors(self) -> None:
        if CORS_ORIGINS:
            self.send_header("Access-Control-Allow-Origin", CORS_ORIGINS)

    def _send_json(self, data: dict):
        encoded = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self._add_cors()
        self.end_headers()
        self.wfile.write(encoded)

    def do_OPTIONS(self):
        self.send_response(204)
        self._add_cors()
        self.send_header(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            self._send_json(health())
            return
        if self.path.startswith("/detect_inventory/"):
            try:
                _check_auth(self.headers)
            except PermissionError:
                self.send_error(401)
                return
            except RuntimeError:
                self.send_error(429, "Rate limit exceeded")
                return
            job_id = self.path.rsplit("/", 1)[-1]
            try:
                job_obj = Job.fetch(job_id, connection=redis_conn)
            except Exception:
                self.send_error(404)
                return
            if job_obj.is_finished:
                self._send_json(job_obj.result)
            elif job_obj.is_failed:
                self.send_error(500, "Job failed")
            else:
                self.send_response(202)
                self._add_cors()
                self.end_headers()
            return
        if self.path.startswith("/generate/"):
            try:
                _check_auth(self.headers)
            except PermissionError:
                self.send_error(401)
                return
            except RuntimeError:
                self.send_error(429, "Rate limit exceeded")
                return
            job_id = self.path.rsplit("/", 1)[-1]
            try:
                job_obj = Job.fetch(job_id, connection=redis_conn)
            except Exception:
                self.send_error(404)
                return
            if job_obj.is_finished:
                self._send_json(job_obj.result)
            elif job_obj.is_failed:
                self.send_error(500, "Job failed")
            else:
                self.send_response(202)
                self._add_cors()
                self.end_headers()
            return
        if self.path.startswith("/progress/"):
            job_id = self.path.split("/", 2)[-1]
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self._add_cors()
            self.end_headers()
            last = None
            while True:
                try:
                    job_obj = Job.fetch(job_id, connection=redis_conn)
                except Exception:
                    break
                prog = job_obj.meta.get("progress")
                if prog != last and prog is not None:
                    data = json.dumps({"progress": prog}).encode()
                    self.wfile.write(b"data: " + data + b"\n\n")
                    self.wfile.flush()
                    last = prog
                if job_obj.is_finished or job_obj.is_failed:
                    break
                time.sleep(1)
            return
        if self.path == "/submissions":
            try:
                _check_admin(self.headers)
            except PermissionError:
                self.send_error(401)
                return
            SUBMISSIONS_ROOT.mkdir(parents=True, exist_ok=True)
            items = []
            for item in sorted(SUBMISSIONS_ROOT.glob("*.json")):
                try:
                    data = json.loads(item.read_text())
                    title = data.get("title", "?")
                    prompt = data.get("prompt", "")
                except Exception:
                    title = "?"
                    prompt = ""
                items.append({"file": item.name, "title": title, "prompt": prompt})
            self._send_json({"submissions": items})
            return
        if self.path.startswith("/comments/"):
            ex_id = self.path.rsplit("/", 1)[-1]
            file_path = COMMENTS_ROOT / f"{ex_id}.json"
            if file_path.is_file():
                try:
                    comments = json.loads(file_path.read_text())
                except Exception:
                    comments = []
            else:
                comments = []
            self._send_json({"comments": comments[-10:]})
            return
        if self.path == "/metrics":
            try:
                _check_admin(self.headers)
            except PermissionError:
                self.send_error(401)
                return
            self._send_json(METRICS)
            return
        if self.path.startswith("/federated_search"):
            query = parse_qs(urlsplit(self.path).query).get("q", [""])[0].lower()
            results = []
            for ex in _local_examples():
                text = f"{ex.get('title','')} {ex.get('prompt','')}".lower()
                if query in text:
                    results.append(ex)
            for base in FEDERATED_INSTANCES:
                for ex in _fetch_examples(base):
                    text = f"{ex.get('title','')} {ex.get('prompt','')}".lower()
                    if query in text:
                        results.append(ex)
            self._send_json({"examples": results})
            return
        if self.path == "/history":
            try:
                _check_auth(self.headers)
            except PermissionError:
                self.send_error(401)
                return
            from backend.history import load

            self._send_json({"history": load()})
            return
        if self.path.startswith("/static/"):
            base = STATIC_ROOT.resolve()
            rel = self.path[len("/static/") :]
            file_path = (base / rel).resolve()
            if not str(file_path).startswith(str(base)) or not file_path.is_file():
                self.send_error(404)
                return
            self.send_response(200)
            if file_path.suffix == ".png":
                content_type = "image/png"
            elif file_path.suffix == ".gltf":
                content_type = "model/gltf+json"
            else:
                content_type = "text/plain"
            self.send_header("Content-Type", content_type)
            data = file_path.read_bytes()
            self.send_header("Content-Length", str(len(data)))
            self._add_cors()
            self.end_headers()
            self.wfile.write(data)
            return
        self.send_error(404)

    def do_POST(self):
        if self.path == "/generate":
            try:
                _check_auth(self.headers)
            except PermissionError:
                self.send_error(401)
                return
            except RuntimeError:
                self.send_error(429, "Rate limit exceeded")
                return
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                payload = json.loads(body.decode() or "{}")
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
                return
            prompt = payload.get("prompt", "")
            seed = payload.get("seed", 42)
            inventory = payload.get("inventory_filter")
            if inventory is not None and not isinstance(inventory, dict):
                self.send_error(400, "Invalid inventory_filter")
                return
            job_obj = queue.enqueue(generate_job, prompt, seed, inventory)
            METRICS["generate_requests"] += 1
            self._send_json({"job_id": job_obj.id})
            return
        if self.path == "/submit_example":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                payload = json.loads(body.decode() or "{}")
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
                return
            title = payload.get("title")
            prompt_text = payload.get("prompt")
            if not title or not prompt_text:
                self.send_error(400, "title and prompt required")
                return
            image = payload.get("image")
            SUBMISSIONS_ROOT.mkdir(parents=True, exist_ok=True)
            from uuid import uuid4

            submission = {"title": title, "prompt": prompt_text}
            if image:
                submission["image"] = image
            (SUBMISSIONS_ROOT / f"{uuid4()}.json").write_text(
                json.dumps(submission, indent=2)
            )
            METRICS["example_submissions"] += 1
            self._send_json({"ok": True})
            return
        if self.path == "/submissions/approve":
            try:
                _check_admin(self.headers)
            except PermissionError:
                self.send_error(401)
                return
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                payload = json.loads(body.decode() or "{}")
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
                return
            file_name = payload.get("file")
            if not file_name:
                self.send_error(400, "file required")
                return
            examples = Path(__file__).resolve().parents[1] / "frontend/public/examples.json"
            from backend.review_cli import approve_submission

            try:
                approve_submission(SUBMISSIONS_ROOT, file_name, examples)
            except Exception:
                self.send_error(400, "invalid submission")
                return
            self._send_json({"ok": True})
            return
        if self.path == "/submissions/reject":
            try:
                _check_admin(self.headers)
            except PermissionError:
                self.send_error(401)
                return
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                payload = json.loads(body.decode() or "{}")
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
                return
            file_name = payload.get("file")
            if not file_name:
                self.send_error(400, "file required")
                return
            file_path = SUBMISSIONS_ROOT / file_name
            if file_path.is_file():
                file_path.unlink()
                self._send_json({"ok": True})
            else:
                self.send_error(404, "file not found")
            return
        if self.path.startswith("/comments/"):
            try:
                _check_auth(self.headers)
            except PermissionError:
                self.send_error(401)
                return
            except RuntimeError:
                self.send_error(429, "Rate limit exceeded")
                return
            ex_id = self.path.rsplit("/", 1)[-1]
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                payload = json.loads(body.decode() or "{}")
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
                return
            text = payload.get("comment")
            if not text:
                self.send_error(400, "comment required")
                return
            COMMENTS_ROOT.mkdir(parents=True, exist_ok=True)
            file_path = COMMENTS_ROOT / f"{ex_id}.json"
            try:
                comments = json.loads(file_path.read_text()) if file_path.is_file() else []
            except Exception:
                comments = []
            try:
                user = decode_jwt(
                    self.headers.get("Authorization", "").split(" ", 1)[1], JWT_SECRET
                ).get("sub", "user")
            except Exception:
                user = "user"
            comments.append({"user": user, "text": text, "ts": int(time.time())})
            file_path.write_text(json.dumps(comments, indent=2))
            try:
                from backend.notify import send_comment_notification

                send_comment_notification(ex_id, user, text)
            except Exception:
                pass
            self._send_json({"ok": True})
            return
        if self.path == "/detect_inventory":
            try:
                _check_auth(self.headers)
            except PermissionError:
                self.send_error(401)
                return
            except RuntimeError:
                self.send_error(429, "Rate limit exceeded")
                return
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                payload = json.loads(body.decode() or "{}")
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
                return
            image_b64 = payload.get("image", "")
            try:
                # Validate base64 before queuing the job
                from backend.detector import _validate_base64

                _validate_base64(image_b64)
            except Exception:
                self.send_error(400, "Invalid image data")
                return
            job_obj = queue.enqueue(detect_job, image_b64)
            METRICS["detect_requests"] += 1
            self._send_json({"job_id": job_obj.id})
            return
        self.send_error(404)


def run(
    host: str = "0.0.0.0",
    port: int = 8000,
    queue_name: str = QUEUE_NAME,
    redis_url: str = REDIS_URL,
    jwt_secret: str = JWT_SECRET,
    rate_limit: int = RATE_LIMIT,
    static_root: str | None = None,
    comments_root: str | None = None,
    log_level: str | None = None,
    log_file: str | None = None,
    cors_origins: str = CORS_ORIGINS,
) -> None:
    """Start the HTTP API server."""
    global queue, redis_conn, JWT_SECRET, RATE_LIMIT, CORS_ORIGINS, COMMENTS_ROOT
    redis_conn = Redis.from_url(redis_url)
    queue = Queue(queue_name, connection=redis_conn)
    JWT_SECRET = jwt_secret
    RATE_LIMIT = rate_limit
    if static_root:
        import backend as backend_pkg

        backend_pkg.STATIC_ROOT = Path(static_root).resolve()
    if comments_root:
        import backend as backend_pkg

        backend_pkg.COMMENTS_ROOT = Path(comments_root).resolve()
    CORS_ORIGINS = cors_origins
    setup_logging(log_level, log_file)
    server = HTTPServer((host, port), Handler)
    print(f"Serving on http://{host}:{port}")
    server.serve_forever()


def main() -> None:
    """Parse CLI args and run the HTTP server."""
    import argparse

    parser = argparse.ArgumentParser(description="Run Lego GPT API server")
    parser.add_argument(
        "--host",
        default=os.getenv("HOST", "0.0.0.0"),
        help="Host interface to bind (default: 0.0.0.0 or HOST env var)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("PORT", "8000")),
        help="Port number (default: 8000 or PORT env var)",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print backend version and exit",
    )
    parser.add_argument(
        "--queue",
        default=os.getenv("QUEUE_NAME", QUEUE_NAME),
        help="RQ queue name (default: env QUEUE_NAME or 'legogpt')",
    )
    parser.add_argument(
        "--redis-url",
        default=os.getenv("REDIS_URL", REDIS_URL),
        help="Redis connection URL (default: env REDIS_URL or redis://localhost:6379/0)",
    )
    parser.add_argument(
        "--jwt-secret",
        default=os.getenv("JWT_SECRET", JWT_SECRET),
        help="JWT secret for request authentication (default: env JWT_SECRET or 'secret')",
    )
    parser.add_argument(
        "--rate-limit",
        type=int,
        default=int(os.getenv("RATE_LIMIT", str(RATE_LIMIT))),
        help="Requests per token per minute (default: env RATE_LIMIT or 5)",
    )
    parser.add_argument(
        "--static-root",
        default=os.getenv("STATIC_ROOT", str(STATIC_ROOT)),
        help=(
            "Directory for generated assets (default: env STATIC_ROOT or "
            "backend/static)"
        ),
    )
    parser.add_argument(
        "--comments-root",
        default=os.getenv("COMMENTS_ROOT", str(COMMENTS_ROOT)),
        help="Directory for example comments (default: env COMMENTS_ROOT)",
    )
    parser.add_argument(
        "--log-level",
        default=os.getenv("LOG_LEVEL", "INFO"),
        help="Logging level (default: env LOG_LEVEL or INFO)",
    )
    parser.add_argument(
        "--log-file",
        default=os.getenv("LOG_FILE"),
        help="File path to write logs (default: env LOG_FILE)",
    )
    parser.add_argument(
        "--cors-origins",
        default=os.getenv("CORS_ORIGINS", CORS_ORIGINS),
        help=(
            "Access-Control-Allow-Origin header value (default: env CORS_ORIGINS or '*')"
        ),
    )
    args = parser.parse_args()
    if args.version:
        print(__version__)
        return
    run(
        args.host,
        args.port,
        args.queue,
        args.redis_url,
        args.jwt_secret,
        args.rate_limit,
        args.static_root,
        args.comments_root,
        args.log_level,
        args.log_file,
        args.cors_origins,
    )


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
