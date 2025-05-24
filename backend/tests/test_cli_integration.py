import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, mock_open
from urllib.error import HTTPError

project_root = Path(__file__).resolve().parents[2]
vendor_root = project_root / "vendor"
for p in (project_root, vendor_root):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import backend.cli as cli


class CLIIntegrationTests(unittest.TestCase):
    def _progress_side_effect(self):
        """Yield 202 then 200 responses for polling."""
        state = {"count": 0}

        class DummyResp(io.BytesIO):
            def __init__(self, status: int, payload: dict):
                super().__init__(json.dumps(payload).encode())
                self.status = status
            def __enter__(self):
                return self
            def __exit__(self, exc_type, exc, tb):
                self.close()

        def side_effect(req, *args, **kwargs):
            # first call after POST raises 202, second returns 200
            if state["count"] % 2 == 0:
                state["count"] += 1
                raise HTTPError(req.full_url, 202, "Accepted", {}, io.BytesIO())
            state["count"] += 1
            return DummyResp(200, {"ok": True})

        return side_effect

    def test_generate_batch_progress(self):
        argv = ["cli", "--token", "tok", "generate", "--file", "prompts.txt"]
        prompts = "one\ntwo\n"
        with patch.object(sys, "argv", argv), \
             patch("backend.cli.open", mock_open(read_data=prompts), create=True), \
             patch("backend.cli._post", side_effect=[{"job_id": "1"}, {"job_id": "2"}]), \
             patch("backend.cli.request.urlopen", side_effect=self._progress_side_effect()), \
             patch("sys.stderr", new=io.StringIO()) as fake_err, \
             patch("sys.stdout", new=io.StringIO()) as fake_out:
            cli.main()
        # two prompts -> two progress dots
        self.assertEqual(fake_err.getvalue().count("."), 2)
        # should print two JSON objects
        out = fake_out.getvalue()
        self.assertEqual(out.count('"ok": true'), 2)

    def test_detect_progress(self):
        argv = ["cli", "--token", "tok", "detect", "img.png"]
        with patch.object(sys, "argv", argv), \
             patch("backend.cli.open", mock_open(read_data=b"img"), create=True), \
             patch("backend.cli._post", return_value={"job_id": "1"}), \
             patch("backend.cli.request.urlopen", side_effect=self._progress_side_effect()), \
             patch("sys.stderr", new=io.StringIO()) as fake_err, \
             patch("sys.stdout", new=io.StringIO()):
            cli.main()
        self.assertEqual(fake_err.getvalue().count("."), 1)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
