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


class ServerTests(unittest.TestCase):
    def setUp(self):
        os.environ["JWT_SECRET"] = "testsecret"
        os.environ["RATE_LIMIT"] = "2"
        import backend.gateway as server_mod

        self.server = importlib.reload(server_mod)
        import tempfile
        from pathlib import Path
        self.tmp_history = Path(tempfile.mkdtemp())
        self.server.HISTORY_ROOT = self.tmp_history
        self.tmp_prefs = Path(tempfile.mkdtemp())
        self.server.PREFERENCES_ROOT = self.tmp_prefs
        self.token = auth.encode({"sub": "t"}, "testsecret")
        self.admin_token = auth.encode({"sub": "a", "role": "admin"}, "testsecret")
        self.httpd = self.server.HTTPServer(("127.0.0.1", 0), self.server.Handler)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever)
        self.thread.start()

    def tearDown(self):
        self.httpd.shutdown()
        self.thread.join()
        # Ensure the server socket is fully closed to avoid resource warnings
        self.httpd.server_close()
        import shutil
        shutil.rmtree(self.tmp_history)
        shutil.rmtree(self.tmp_prefs)

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
        status, _ = self._request("GET", "/static/../gateway.py")
        self.assertEqual(status, 404)

    @patch("backend.gateway.queue")
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
        mock_queue.enqueue.assert_called_once()

    @patch("backend.gateway.queue")
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

    @patch("backend.gateway.queue")
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

    @patch("backend.gateway.queue")
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

    @patch("backend.gateway.queue")
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

    def test_submit_example_post(self):
        import tempfile
        import shutil
        from pathlib import Path

        tmp = Path(tempfile.mkdtemp())
        self.server.SUBMISSIONS_ROOT = tmp
        class FakeRedis:
            def __init__(self):
                self.items = []
            def rpush(self, key, val):
                self.items.append(val)
            def lrange(self, key, start, end):
                return self.items[start : end + 1 if end != -1 else None]
            def lrem(self, key, count, val):
                self.items = [v for v in self.items if v != val]

        self.server.submissions_redis = FakeRedis()
        payload = {"title": "x", "prompt": "y"}
        status, data = self._request(
            "POST", "/submit_example", body=json.dumps(payload).encode()
        )
        self.assertEqual(status, 200)
        files = list(tmp.glob("*.json"))
        self.assertEqual(len(files), 1)
        obj = json.loads(files[0].read_text())
        self.assertEqual(obj["title"], "x")
        self.assertEqual(len(self.server.submissions_redis.items), 1)
        shutil.rmtree(tmp)

    def test_submissions_get_redis(self):
        self.server.SUBMISSIONS_ROOT.mkdir(parents=True, exist_ok=True)
        class FakeRedis:
            def __init__(self, items):
                self.items = items
            def lrange(self, key, start, end):
                return [i.encode() for i in self.items]
        fname = "s1.json"
        (self.server.SUBMISSIONS_ROOT / fname).write_text(json.dumps({"title": "t"}))
        self.server.submissions_redis = FakeRedis([fname])
        status, data = self._request("GET", "/submissions", token=self.admin_token)
        self.assertEqual(status, 200)
        subs = json.loads(data)["submissions"]
        self.assertEqual(len(subs), 1)

    def test_submit_example_missing(self):
        status, _ = self._request(
            "POST", "/submit_example", body=b"{}"
        )
        self.assertEqual(status, 400)

    def test_comments_post_and_get(self):
        import tempfile
        from pathlib import Path

        tmp = Path(tempfile.mkdtemp())
        self.server.COMMENTS_ROOT = tmp
        status, _ = self._request(
            "POST",
            "/comments/1",
            body=b'{"comment":"nice"}',
            token=self.token,
        )
        self.assertEqual(status, 200)
        status, data = self._request("GET", "/comments/1")
        self.assertEqual(status, 200)
        payload = json.loads(data)
        self.assertEqual(payload["comments"][0]["text"], "nice")

    @patch("backend.notify.send_comment_notification")
    def test_comments_post_triggers_notification(self, mock_notify):
        import tempfile
        from pathlib import Path

        tmp = Path(tempfile.mkdtemp())
        self.server.COMMENTS_ROOT = tmp
        status, _ = self._request(
            "POST",
            "/comments/2",
            body=b'{"comment":"great"}',
            token=self.token,
        )
        self.assertEqual(status, 200)
        mock_notify.assert_called_once()

    def test_metrics_endpoint(self):
        with patch("backend.gateway.queue.enqueue") as mock_q:
            mock_q.return_value.id = "j"
            self._request("POST", "/generate", body=b"{}", token=self.token)
            self._request("POST", "/detect_inventory", body=b'{"image":"d"}', token=self.token)
        status, _ = self._request("GET", "/metrics", token=self.token)
        self.assertEqual(status, 401)
        status, data = self._request("GET", "/metrics", token=self.admin_token)
        self.assertEqual(status, 200)
        payload = json.loads(data)
        self.assertGreaterEqual(payload.get("generate_requests", 0), 1)

    @patch("backend.gateway.Job.fetch")
    def test_progress_events(self, mock_fetch):
        state = {"calls": 0}

        def fake_fetch(job_id, connection=None):
            class Dummy:
                pass

            obj = Dummy()

            call = state["calls"]
            state["calls"] += 1

            obj.meta = {"progress": 0 if call == 0 else 100}
            obj.is_failed = False
            obj.is_finished = call > 0
            return obj

        mock_fetch.side_effect = fake_fetch
        status, data, headers = self._request_full("GET", "/progress/1")
        self.assertEqual(status, 200)
        self.assertEqual(headers.get("Content-Type"), "text/event-stream")
        self.assertIn(b"progress", data)

    def test_history_endpoint(self):
        # Simulate finished job and ensure history is recorded
        with patch("backend.gateway.Job.fetch") as mock_fetch, patch("backend.gateway.queue.enqueue") as mock_q:
            class DummyJob:
                def __init__(self):
                    self.id = "1"
                    self.meta = {"user": "t", "prompt": "p", "seed": 1}
                    self.result = {"png_url": "u"}
                    self.is_finished = True
                    self.is_failed = False
                def save_meta(self):
                    pass
            job = DummyJob()
            mock_q.return_value = job
            self._request("POST", "/generate", body=b'{"prompt":"p","seed":1}', token=self.token)
            mock_fetch.return_value = job
            self._request("GET", f"/generate/{job.id}", token=self.token)
        self.server._TOKEN_USAGE.clear()
        status, _ = self._request("GET", "/history", token=self.token)
        self.assertEqual(status, 200)

    def test_federated_search(self):
        with patch("urllib.request.urlopen") as mock_urlopen:
            class Resp:
                def __init__(self, data):
                    self.data = data
                def read(self):
                    return json.dumps([{"id": "2", "title": "R", "prompt": "p"}]).encode()
                def __enter__(self):
                    return self
                def __exit__(self, exc_type, exc, tb):
                    pass

            mock_urlopen.return_value = Resp([])
            self.server.EXAMPLE_SOURCES = ["http://x"]
            status, data = self._request("GET", "/search_examples?q=p")
        self.assertEqual(status, 200)
        payload = json.loads(data)
        self.assertGreaterEqual(len(payload["examples"]), 1)

    def test_link_code_and_preferences(self):
        self.server._TOKEN_USAGE.clear()
        self.server.RATE_LIMIT = 10
        # Generate a link code
        status, data = self._request(
            "POST", "/link_code", token=self.token
        )
        self.assertEqual(status, 200)
        code = json.loads(data)["code"]
        # Consume the code
        status, data = self._request("GET", f"/link_account?code={code}")
        self.assertEqual(status, 200)
        token = json.loads(data)["token"]
        self.assertEqual(token, self.token)
        # Preferences round trip
        pref_body = json.dumps({"email": True}).encode()
        status, _ = self._request(
            "POST", "/preferences", body=pref_body, token=self.token
        )
        self.assertEqual(status, 200)
        status, data = self._request("GET", "/preferences", token=self.token)
        self.assertEqual(status, 200)
        prefs = json.loads(data)["preferences"]
        self.assertTrue(prefs.get("email"))

    def test_report_and_metrics(self):
        import tempfile
        from pathlib import Path

        tmp = Path(tempfile.mkdtemp())
        self.server.REPORTS_ROOT = tmp
        status, _ = self._request("POST", "/report", body=b'{"id":"1"}', token=self.token)
        self.assertEqual(status, 200)
        status, data = self._request("GET", "/reports", token=self.admin_token)
        self.assertEqual(status, 200)
        payload = json.loads(data)
        self.assertEqual(payload["reports"][0]["id"], "1")

    def test_ban_user_and_comment_delete(self):
        import tempfile
        from pathlib import Path

        self.server._TOKEN_USAGE.clear()
        tmpc = Path(tempfile.mkdtemp())
        self.server.COMMENTS_ROOT = tmpc
        tmpb = Path(tempfile.mkdtemp()) / "b.json"
        self.server.BANS_FILE = tmpb
        status, _ = self._request("POST", "/comments/2", body=b'{"comment":"hi"}', token=self.token)
        self.assertEqual(status, 200)
        status, _ = self._request("POST", "/comments/2/delete", body=b'{"index":0}', token=self.admin_token)
        self.assertEqual(status, 200)
        status, data = self._request("GET", "/comments/2")
        self.assertEqual(json.loads(data)["comments"], [])
        status, _ = self._request("POST", "/ban_user", body=b'{"user":"t"}', token=self.admin_token)
        self.assertEqual(status, 200)
        status, _ = self._request("POST", "/generate", body=b"{}", token=self.token)
        self.assertEqual(status, 401)

    def test_rate_limit_metrics(self):
        self.server.RATE_LIMIT = 1
        self.server._TOKEN_USAGE.clear()
        with patch("backend.gateway.queue.enqueue") as mock_q:
            mock_q.return_value.id = "j"
            self._request("POST", "/generate", body=b"{}", token=self.token)
        self._request("POST", "/generate", body=b"{}", token=self.token)
        status, data = self._request("GET", "/metrics", token=self.admin_token)
        payload = json.loads(data)
        self.assertGreaterEqual(payload.get("token_usage", 0), 1)
        self.assertGreaterEqual(payload.get("rate_limit_hits", 0), 1)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
