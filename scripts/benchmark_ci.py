#!/usr/bin/env python3
"""Run scalability benchmark using a lightweight stub server."""
import json
import threading
import time
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from scripts import benchmark_scalability

_JOBS: dict[str, dict] = {}

class Handler(BaseHTTPRequestHandler):
    def _send_json(self, data: dict, status: int = 200) -> None:
        encoded = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_POST(self) -> None:  # type: ignore[override]
        if self.path != "/generate":
            self.send_error(404)
            return
        # discard body
        length = int(self.headers.get("Content-Length", 0))
        if length:
            self.rfile.read(length)
        job_id = str(uuid.uuid4())
        threading.Thread(target=self._complete_job, args=(job_id,), daemon=True).start()
        self._send_json({"job_id": job_id})

    def _complete_job(self, job_id: str) -> None:
        time.sleep(0.05)
        _JOBS[job_id] = {
            "png_url": "/static/dummy.png",
            "ldr_url": None,
            "gltf_url": None,
            "brick_counts": {},
        }

    def do_GET(self) -> None:  # type: ignore[override]
        if not self.path.startswith("/generate/"):
            self.send_error(404)
            return
        job_id = self.path.rsplit("/", 1)[-1]
        job = _JOBS.get(job_id)
        if not job:
            self.send_response(202)
            self.end_headers()
            return
        self._send_json(job)

    def log_message(self, format: str, *args) -> None:  # noqa: D401
        # silence default logging for cleaner CI output
        return

def main() -> None:
    server = HTTPServer(("127.0.0.1", 8000), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        benchmark_scalability.benchmark(
            "http://127.0.0.1:8000", "dummy", "bench", 42, requests=10, concurrency=2
        )
    finally:
        server.shutdown()
        thread.join()

if __name__ == "__main__":  # pragma: no cover - manual script
    main()
