import os
import sys
import threading
import http.client
import json
from pathlib import Path
from unittest.mock import MagicMock, patch
import unittest

# Ensure project and vendor are on sys.path
project_root = Path(__file__).resolve().parents[2]
vendor_root = project_root / "vendor"
for p in (project_root, vendor_root):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
os.environ["PYTHONPATH"] = str(project_root)

from backend import server  # noqa: E402


class ServerTests(unittest.TestCase):
    def setUp(self):
        self.httpd = server.HTTPServer(("127.0.0.1", 0), server.Handler)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever)
        self.thread.start()

    def tearDown(self):
        self.httpd.shutdown()
        self.thread.join()
        # Ensure the server socket is fully closed to avoid resource warnings
        self.httpd.server_close()

    def _request(self, method: str, path: str, body: bytes | None = None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port)
        conn.request(method, path, body)
        resp = conn.getresponse()
        data = resp.read()
        conn.close()
        return resp.status, data

    def test_health_endpoint(self):
        status, data = self._request("GET", "/health")
        self.assertEqual(status, 200)
        payload = json.loads(data)
        self.assertTrue(payload.get("ok"))

    @patch("backend.server.queue")
    def test_generate_post(self, mock_queue):
        mock_job = MagicMock(id="abc")
        mock_queue.enqueue.return_value = mock_job

        status, data = self._request(
            "POST",
            "/generate",
            body=b'{"prompt":"cube","seed":1}'
        )
        self.assertEqual(status, 200)
        payload = json.loads(data)
        self.assertEqual(payload["job_id"], "abc")
        mock_queue.enqueue.assert_called_once()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
