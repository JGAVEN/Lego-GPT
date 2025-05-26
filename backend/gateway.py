"""Tiny HTTP server exposing the Lego GPT API via an RQ queue."""

import json
import os
import time
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from redis import Redis
from rq import Queue, Job, Retry
from backend.api import health
from backend import (
    STATIC_ROOT,
    SUBMISSIONS_ROOT,
    SUBMISSIONS_REDIS_URL,
    COMMENTS_ROOT,
    REPORTS_ROOT,
    BANS_FILE,
    HISTORY_ROOT,
    PREFERENCES_ROOT,
)
from backend.worker import QUEUE_NAME as DEFAULT_QUEUE, generate_job, detect_job
from backend.auth import decode as decode_jwt
from backend import __version__
from backend.logging_config import setup_logging


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_conn = Redis.from_url(REDIS_URL)
submissions_redis = Redis.from_url(SUBMISSIONS_REDIS_URL) if SUBMISSIONS_REDIS_URL else None
QUEUE_NAME = os.getenv("QUEUE_NAME", DEFAULT_QUEUE)
queue = Queue(QUEUE_NAME, connection=redis_conn)
DEFAULT_RETRY = Retry(max=3, interval=[10, 30, 60])

JWT_SECRET = os.getenv("JWT_SECRET", "secret")
RATE_LIMIT = int(os.getenv("RATE_LIMIT", "5"))
# Allow cross-origin requests
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
# token -> (count, window_epoch_minute)
# token -> (count, window_epoch_minute)
_TOKEN_USAGE: dict[str, tuple[int, int]] = {}
# one-time link codes -> (token, expiry_ts)
_LINK_CODES: dict[str, tuple[str, float]] = {}

# banned user subjects
_BANNED_USERS: set[str] = set()

# Simple in-memory metrics
METRICS = {
    "generate_requests": 0,
    "detect_requests": 0,
    "example_submissions": 0,
    "example_reports": 0,
    "token_usage": 0,
    "rate_limit_hits": 0,
}

# Sliding-window metric history (last 60 minutes)
METRICS_HISTORY: dict[str, dict[int, int]] = {
    "token_usage": {},
    "rate_limit_hits": {},
}


def _record_history(key: str) -> None:
    """Increment minute bucket for ``key`` and trim old entries."""
    now_min = int(time.time() // 60)
    hist = METRICS_HISTORY.setdefault(key, {})
    hist[now_min] = hist.get(now_min, 0) + 1
    for ts in list(hist):
        if now_min - ts > 59:
            del hist[ts]

# Additional example sources for federated search
EXAMPLE_SOURCES = [s for s in os.getenv("EXAMPLE_SOURCES", "").split(",") if s]

if BANS_FILE.is_file():
    try:
        _BANNED_USERS.update(json.loads(BANS_FILE.read_text()))
    except Exception:
        pass


def _check_auth(headers) -> None:
    auth = headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise PermissionError
    token = auth.split(" ", 1)[1]
    payload = decode_jwt(token, JWT_SECRET)
    if payload.get("sub") in _BANNED_USERS:
        raise PermissionError

    METRICS["token_usage"] += 1
    _record_history("token_usage")

    now = int(time.time())
    window = now // 60
    count, win = _TOKEN_USAGE.get(token, (0, window))
    if win != window:
        count = 0
        win = window
    if count >= RATE_LIMIT:
        METRICS["rate_limit_hits"] += 1
        _record_history("rate_limit_hits")
        raise RuntimeError("rate_limit")
    _TOKEN_USAGE[token] = (count + 1, win)


def _search_examples(query: str) -> list[dict]:
    """Search local and remote examples for ``query``."""
    examples_file = Path(__file__).resolve().parents[1] / "frontend/public/examples.json"
    try:
        data = json.loads(examples_file.read_text())
    except Exception:
        data = []
    results = []
    q = query.lower()
    for ex in data:
        text = f"{ex.get('title','')} {ex.get('prompt','')}".lower()
        if q in text:
            ex = ex.copy()
            ex["source"] = "local"
            results.append(ex)
    for base in EXAMPLE_SOURCES:
        url = base.rstrip("/") + "/examples.json"
        try:
            import urllib.request

            with urllib.request.urlopen(url, timeout=2) as resp:
                remote = json.loads(resp.read().decode())
        except Exception:
            continue
        for ex in remote:
            text = f"{ex.get('title','')} {ex.get('prompt','')}".lower()
            if q in text:
                ex = ex.copy()
                ex["source"] = base
                results.append(ex)
    return results


def _check_admin(headers) -> None:
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
                result = job_obj.result
                self._send_json(result)
                user = job_obj.meta.get("user")
                if user:
                    HISTORY_ROOT.mkdir(parents=True, exist_ok=True)
                    file_path = HISTORY_ROOT / f"{user}.jsonl"
                    record = {
                        "prompt": job_obj.meta.get("prompt", ""),
                        "seed": job_obj.meta.get("seed", 42),
                        "result": result,
                        "ts": int(time.time()),
                    }
                    with open(file_path, "a") as fh:
                        fh.write(json.dumps(record) + "\n")
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
            if submissions_redis:
                try:
                    names = [n.decode() for n in submissions_redis.lrange("submissions", 0, -1)]
                except Exception:
                    names = []
            else:
                names = [p.name for p in sorted(SUBMISSIONS_ROOT.glob("*.json"))]
            items = []
            for fname in names:
                item = SUBMISSIONS_ROOT / fname
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
        if self.path == "/reports":
            try:
                _check_admin(self.headers)
            except PermissionError:
                self.send_error(401)
                return
            REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
            items = []
            for p in sorted(REPORTS_ROOT.glob("*.json")):
                try:
                    data = json.loads(p.read_text())
                    count = len(data)
                except Exception:
                    count = 0
                items.append({"id": p.stem, "count": count})
            self._send_json({"reports": items})
            return
        if self.path == "/bans":
            try:
                _check_admin(self.headers)
            except PermissionError:
                self.send_error(401)
                return
            self._send_json({"bans": sorted(_BANNED_USERS)})
            return
        if self.path == "/metrics":
            try:
                _check_admin(self.headers)
            except PermissionError:
                self.send_error(401)
                return
            payload = dict(METRICS)
            payload["history"] = {
                k: sorted(v.items()) for k, v in METRICS_HISTORY.items()
            }
            self._send_json(payload)
            return
        if self.path.startswith("/search_examples"):
            q = self.path.split("?q=", 1)[-1] if "?q=" in self.path else ""
            if not q:
                self.send_error(400, "q required")
                return
            self._send_json({"examples": _search_examples(q)})
            return
        if self.path == "/history":
            try:
                _check_auth(self.headers)
            except PermissionError:
                self.send_error(401)
                return
            token = self.headers.get("Authorization", "").split(" ", 1)[1]
            user = decode_jwt(token, JWT_SECRET).get("sub", "user")
            file_path = HISTORY_ROOT / f"{user}.jsonl"
            if file_path.is_file():
                entries = [json.loads(line) for line in file_path.read_text().splitlines()]
            else:
                entries = []
            self._send_json({"history": entries})
            return
        if self.path.startswith("/link_account"):
            code = self.path.split("?code=", 1)[-1] if "?code=" in self.path else ""
            token = None
            if code and code in _LINK_CODES:
                t, exp = _LINK_CODES.pop(code)
                if time.time() < exp:
                    token = t
            if token:
                self._send_json({"token": token})
            else:
                self.send_error(404)
            return
        if self.path == "/preferences":
            try:
                _check_auth(self.headers)
            except PermissionError:
                self.send_error(401)
                return
            token = self.headers.get("Authorization", "").split(" ", 1)[1]
            user = decode_jwt(token, JWT_SECRET).get("sub", "user")
            pref_path = PREFERENCES_ROOT / f"{user}.json"
            if pref_path.is_file():
                try:
                    data = json.loads(pref_path.read_text())
                except Exception:
                    data = {}
            else:
                data = {}
            self._send_json({"preferences": data})
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
        if self.path == "/link_code":
            try:
                _check_auth(self.headers)
            except PermissionError:
                self.send_error(401)
                return
            token = self.headers.get("Authorization", "").split(" ", 1)[1]
            import random
            import string

            code = "".join(random.choices(string.digits, k=6))
            _LINK_CODES[code] = (token, time.time() + 600)
            self._send_json({"code": code})
            return
        if self.path == "/preferences":
            try:
                _check_auth(self.headers)
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
            token = self.headers.get("Authorization", "").split(" ", 1)[1]
            user = decode_jwt(token, JWT_SECRET).get("sub", "user")
            pref_path = PREFERENCES_ROOT / f"{user}.json"
            PREFERENCES_ROOT.mkdir(parents=True, exist_ok=True)
            pref_path.write_text(json.dumps(payload, indent=2))
            self._send_json({"ok": True})
            return
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
            token = self.headers.get("Authorization", "").split(" ", 1)[1]
            payload = decode_jwt(token, JWT_SECRET)
            job_obj = queue.enqueue(
                generate_job, prompt, seed, inventory, retry=DEFAULT_RETRY
            )
            job_obj.meta["user"] = payload.get("sub", "user")
            job_obj.meta["prompt"] = prompt
            job_obj.meta["seed"] = seed
            job_obj.save_meta()
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
            file_name = f"{uuid4()}.json"
            (SUBMISSIONS_ROOT / file_name).write_text(
                json.dumps(submission, indent=2)
            )
            if submissions_redis:
                try:
                    submissions_redis.rpush("submissions", file_name)
                except Exception:
                    pass
            METRICS["example_submissions"] += 1
            self._send_json({"ok": True})
            return
        if self.path == "/report":
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
            ex_id = payload.get("id")
            if not ex_id:
                self.send_error(400, "id required")
                return
            REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
            file_path = REPORTS_ROOT / f"{ex_id}.json"
            try:
                reports = json.loads(file_path.read_text()) if file_path.is_file() else []
            except Exception:
                reports = []
            user = decode_jwt(self.headers.get("Authorization", "").split(" ", 1)[1], JWT_SECRET).get("sub", "user")
            reports.append({"user": user, "ts": int(time.time())})
            file_path.write_text(json.dumps(reports, indent=2))
            METRICS["example_reports"] += 1
            self._send_json({"ok": True})
            return
        if self.path == "/reports/clear":
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
            rep_id = payload.get("id")
            if not rep_id:
                self.send_error(400, "id required")
                return
            file_path = REPORTS_ROOT / f"{rep_id}.json"
            if file_path.is_file():
                file_path.unlink()
                self._send_json({"ok": True})
            else:
                self.send_error(404, "report not found")
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
            if submissions_redis:
                try:
                    submissions_redis.lrem("submissions", 0, file_name)
                except Exception:
                    pass
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
                if submissions_redis:
                    try:
                        submissions_redis.lrem("submissions", 0, file_name)
                    except Exception:
                        pass
                self._send_json({"ok": True})
            else:
                self.send_error(404, "file not found")
            return
        if self.path == "/ban_user":
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
            user = payload.get("user")
            if not user:
                self.send_error(400, "user required")
                return
            _BANNED_USERS.add(user)
            try:
                BANS_FILE.write_text(json.dumps(sorted(_BANNED_USERS), indent=2))
            except Exception:
                pass
            self._send_json({"ok": True})
            return
        if self.path == "/bans":
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
            items = payload.get("bans")
            if not isinstance(items, list):
                self.send_error(400, "bans required")
                return
            for u in items:
                _BANNED_USERS.add(str(u))
            try:
                BANS_FILE.write_text(json.dumps(sorted(_BANNED_USERS), indent=2))
            except Exception:
                pass
            self._send_json({"ok": True})
            return
        if self.path.startswith("/comments/") and self.path.endswith("/delete"):
            try:
                _check_admin(self.headers)
            except PermissionError:
                self.send_error(401)
                return
            ex_id = self.path.split("/")[2]
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                payload = json.loads(body.decode() or "{}")
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
                return
            idx = payload.get("index")
            if idx is None:
                self.send_error(400, "index required")
                return
            file_path = COMMENTS_ROOT / f"{ex_id}.json"
            try:
                comments = json.loads(file_path.read_text()) if file_path.is_file() else []
            except Exception:
                comments = []
            if 0 <= idx < len(comments):
                comments.pop(idx)
                file_path.write_text(json.dumps(comments, indent=2))
                self._send_json({"ok": True})
            else:
                self.send_error(404, "comment not found")
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
            job_obj = queue.enqueue(detect_job, image_b64, retry=DEFAULT_RETRY)
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
    submissions_redis_url: str | None = None,
    preferences_root: str | None = None,
    log_level: str | None = None,
    log_file: str | None = None,
    cors_origins: str = CORS_ORIGINS,
) -> None:
    """Start the HTTP API server."""
    global queue, redis_conn, JWT_SECRET, RATE_LIMIT, CORS_ORIGINS, COMMENTS_ROOT, submissions_redis, PREFERENCES_ROOT
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
    if submissions_redis_url:
        submissions_redis = Redis.from_url(submissions_redis_url)
    if preferences_root:
        import backend as backend_pkg

        backend_pkg.PREFERENCES_ROOT = Path(preferences_root).resolve()
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
        "--submissions-redis",
        default=os.getenv("SUBMISSIONS_REDIS_URL", SUBMISSIONS_REDIS_URL or ""),
        help="Redis URL for moderation queue (default: env SUBMISSIONS_REDIS_URL)",
    )
    parser.add_argument(
        "--preferences-root",
        default=os.getenv("PREFERENCES_ROOT", str(PREFERENCES_ROOT)),
        help="Directory for user preferences (default: env PREFERENCES_ROOT)",
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
        args.submissions_redis,
        args.preferences_root,
        args.log_level,
        args.log_file,
        args.cors_origins,
    )


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
