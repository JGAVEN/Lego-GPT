"""Tiny HTTP server exposing the Lego GPT API via an RQ queue."""

import json
import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from redis import Redis
from rq import Queue, Job
from backend.api import health, STATIC_ROOT
from backend.worker import QUEUE_NAME, generate_job, detect_job
from backend.auth import decode as decode_jwt


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_conn = Redis.from_url(REDIS_URL)
queue = Queue(QUEUE_NAME, connection=redis_conn)

JWT_SECRET = os.getenv("JWT_SECRET", "secret")
RATE_LIMIT = int(os.getenv("RATE_LIMIT", "5"))
# token -> (count, window_epoch_minute)
_TOKEN_USAGE: dict[str, tuple[int, int]] = {}


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


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, data: dict):
        encoded = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

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
                self.end_headers()
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
                self.send_header("Content-Type", "image/png")
            else:
                self.send_header("Content-Type", "text/plain")
            data = file_path.read_bytes()
            self.send_header("Content-Length", str(len(data)))
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
            self._send_json({"job_id": job_obj.id})
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
            job_obj = queue.enqueue(detect_job, image_b64)
            self._send_json({"job_id": job_obj.id})
            return
        self.send_error(404)


def run(host: str = "0.0.0.0", port: int = 8000):
    """Start the HTTP API server."""
    server = HTTPServer((host, port), Handler)
    print(f"Serving on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
