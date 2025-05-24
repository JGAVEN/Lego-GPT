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

import importlib
from backend import auth
import backend.worker


class ServerTests(unittest.TestCase):
    def setUp(self):
        os.environ["JWT_SECRET"] = "testsecret"
        os.environ["RATE_LIMIT"] = "2"
        import backend.server as server_mod

        self.server = importlib.reload(server_mod)
        self.token = auth.encode({"sub": "t"}, "testsecret")
        self.httpd = self.server.HTTPServer(("127.0.0.1", 0), self.server.Handler)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever)
        self.thread.start()

    def tearDown(self):
        self.httpd.shutdown()
        self.thread.join()
        # Ensure the server socket is fully closed to avoid resource warnings
        self.httpd.server_close()

    def _request(
        self,
        method: str,
        path: str,
        body: bytes | None = None,
        token: str | None = None,
    ):
        conn = http.client.HTTPConnection("127.0.0.1", self.port)
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        conn.request(method, path, body, headers)
        resp = conn.getresponse()
        data = resp.read()
        conn.close()
        return resp.status, data

    def _request_full(
        self,
        method: str,
        path: str,
        body: bytes | None = None,
        token: str | None = None,
    ):
        conn = http.client.HTTPConnection("127.0.0.1", self.port)
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        conn.request(method, path, body, headers)
        resp = conn.getresponse()
        data = resp.read()
        hdrs = dict(resp.getheaders())
        conn.close()
        return resp.status, data, hdrs

    def test_health_endpoint(self):
        status, data = self._request("GET", "/health")
        self.assertEqual(status, 200)
        payload = json.loads(data)
        self.assertTrue(payload.get("ok"))
        self.assertRegex(payload.get("version", ""), r"\d+\.\d+\.\d+")

    def test_static_path_traversal_blocked(self):
        status, _ = self._request("GET", "/static/../server.py")
        self.assertEqual(status, 404)

    @patch("backend.server.queue")
    def test_generate_post(self, mock_queue):
        mock_job = MagicMock(id="abc")
        mock_queue.enqueue.return_value = mock_job

        status, data = self._request(
            "POST",
            "/generate",
            body=b'{"prompt":"cube","seed":1,"inventory_filter":{"Brick":1}}',
            token=self.token,
        )
        self.assertEqual(status, 200)
        payload = json.loads(data)
        self.assertEqual(payload["job_id"], "abc")
        mock_queue.enqueue.assert_called_once_with(
            backend.worker.generate_job,
            "cube",
            1,
            {"Brick": 1},
        )

    @patch("backend.server.queue")
    def test_generate_bad_inventory(self, mock_queue):
        mock_job = MagicMock(id="abc")
        mock_queue.enqueue.return_value = mock_job

        status, _ = self._request(
            "POST",
            "/generate",
            body=b'{"prompt":"cube","inventory_filter":123}',
            token=self.token,
        )
        self.assertEqual(status, 400)
        mock_queue.enqueue.assert_not_called()

    def test_generate_requires_auth(self):
        status, _ = self._request(
            "POST",
            "/generate",
            body=b"{}",
        )
        self.assertEqual(status, 401)

    @patch("backend.server.queue")
    def test_generate_rate_limit(self, mock_queue):
        mock_job = MagicMock(id="abc")
        mock_queue.enqueue.return_value = mock_job
        for _ in range(2):
            status, _ = self._request(
                "POST",
                "/generate",
                body=b"{}",
                token=self.token,
            )
            self.assertEqual(status, 200)
        status, _ = self._request(
            "POST",
            "/generate",
            body=b"{}",
            token=self.token,
        )
        self.assertEqual(status, 429)

    @patch("backend.server.queue")
    def test_detect_inventory_post(self, mock_queue):
        mock_job = MagicMock(id="xyz")
        mock_queue.enqueue.return_value = mock_job

        status, data = self._request(
            "POST",
            "/detect_inventory",
            body=b'{"image":"data"}',
            token=self.token,
        )
        self.assertEqual(status, 200)
        payload = json.loads(data)
        self.assertEqual(payload["job_id"], "xyz")
        mock_queue.enqueue.assert_called_once()

    @patch("backend.server.queue")
    def test_detect_inventory_invalid_base64(self, mock_queue):
        mock_job = MagicMock(id="xyz")
        mock_queue.enqueue.return_value = mock_job

        status, _ = self._request(
            "POST",
            "/detect_inventory",
            body=b'{"image":"@@@"}',
            token=self.token,
        )
        self.assertEqual(status, 400)
        mock_queue.enqueue.assert_not_called()

    def test_options_cors_headers(self):
        status, _, headers = self._request_full("OPTIONS", "/generate")
        self.assertEqual(status, 204)
        self.assertEqual(headers.get("Access-Control-Allow-Origin"), "*")
        self.assertIn("POST", headers.get("Access-Control-Allow-Methods", ""))

    def test_static_gltf_content_type(self):
        import tempfile
        import shutil
        from pathlib import Path

        tmp = Path(tempfile.mkdtemp())
        gltf_dir = tmp / "x"
        gltf_dir.mkdir(parents=True, exist_ok=True)
        (gltf_dir / "model.gltf").write_text("{}")
        self.server.STATIC_ROOT = tmp.resolve()

        status, _, headers = self._request_full("GET", "/static/x/model.gltf")
        self.assertEqual(status, 200)
        self.assertEqual(headers.get("Content-Type"), "model/gltf+json")
        shutil.rmtree(tmp)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
