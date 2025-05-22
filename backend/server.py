"""Tiny HTTP server exposing the Lego GPT API offline."""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from backend.api import health, generate_lego_model, STATIC_ROOT


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
        if self.path.startswith("/static/"):
            file_path = STATIC_ROOT.parent / self.path.lstrip("/")
            if file_path.exists():
                self.send_response(200)
                if file_path.suffix == ".png":
                    self.send_header("Content-Type", "image/png")
                else:
                    self.send_header("Content-Type", "text/plain")
                data = file_path.read_bytes()
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            else:
                self.send_error(404)
            return
        self.send_error(404)

    def do_POST(self):
        if self.path == "/generate":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                payload = json.loads(body.decode() or "{}")
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
                return
            prompt = payload.get("prompt", "")
            seed = payload.get("seed", 42)
            data = generate_lego_model(prompt, seed)
            self._send_json(data)
            return
        self.send_error(404)


def run(host: str = "0.0.0.0", port: int = 8000):
    server = HTTPServer((host, port), Handler)
    print(f"Serving on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
