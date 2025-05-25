import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, mock_open

project_root = Path(__file__).resolve().parents[2]
vendor_root = project_root / "vendor"
for p in (project_root, vendor_root):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import backend.cli as cli


class CLIIntegrationTests(unittest.TestCase):
    class DummyResp(io.BytesIO):
        def __init__(self, payload: bytes):
            super().__init__(payload)
            self.status = 200

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            self.close()

    def test_generate_batch_progress(self):
        argv = ["cli", "--token", "tok", "generate", "--file", "prompts.txt"]
        prompts = "one\ntwo\n"
        with patch.object(sys, "argv", argv), \
             patch("backend.cli.open", mock_open(read_data=prompts), create=True), \
             patch("backend.cli._post", side_effect=[{"job_id": "1"}, {"job_id": "2"}]), \
             patch("backend.cli._stream_progress", side_effect=lambda url: print("..", end="", file=sys.stderr)), \
             patch("backend.cli.request.urlopen", side_effect=lambda *a, **k: self.DummyResp(b'{"ok": true}')), \
             patch("sys.stderr", new=io.StringIO()) as fake_err, \
             patch("sys.stdout", new=io.StringIO()) as fake_out:
            cli.main()
        # progress dots printed
        self.assertGreaterEqual(fake_err.getvalue().count("."), 4)
        # should print two JSON objects
        out = fake_out.getvalue()
        self.assertEqual(out.count('"ok": true'), 2)

    def test_detect_progress(self):
        argv = ["cli", "--token", "tok", "detect", "img.png"]
        with patch.object(sys, "argv", argv), \
             patch("backend.cli.open", mock_open(read_data=b"img"), create=True), \
             patch("backend.cli._post", return_value={"job_id": "1"}), \
             patch("backend.cli._stream_progress", side_effect=lambda url: print("..", end="", file=sys.stderr)), \
             patch("backend.cli.request.urlopen", side_effect=lambda *a, **k: self.DummyResp(b'{"ok": true}')), \
             patch("sys.stderr", new=io.StringIO()) as fake_err, \
             patch("sys.stdout", new=io.StringIO()):
            cli.main()
        self.assertGreaterEqual(fake_err.getvalue().count("."), 2)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
