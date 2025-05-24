import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, mock_open

project_root = Path(__file__).resolve().parents[2]
vendor_root = project_root / "vendor"
for p in (project_root, vendor_root):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import backend
import backend.cli as cli


class APIClientCLITests(unittest.TestCase):
    def test_version_flag(self):
        with patch.object(sys, "argv", ["cli", "--version"]):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                cli.main()
                self.assertEqual(fake_out.getvalue().strip(), backend.__version__)

    def test_generate_command(self):
        argv = ["cli", "--token", "tok", "generate", "hello"]
        with patch.object(sys, "argv", argv), \
             patch("backend.cli._post", return_value={"job_id": "1"}) as mock_post, \
             patch("backend.cli._poll", return_value={"ok": True}) as mock_poll, \
             patch("sys.stdout", new=io.StringIO()):
            cli.main()
        mock_post.assert_called_once()
        mock_poll.assert_called_once()

    def test_generate_with_inventory(self):
        argv = [
            "cli",
            "--token",
            "tok",
            "generate",
            "hello",
            "--inventory",
            "inv.json",
        ]
        inv = {"3001.DAT": 1}
        with patch.object(sys, "argv", argv), \
             patch("backend.cli.open", mock_open(read_data=json.dumps(inv)), create=True), \
             patch("backend.cli._post", return_value={"job_id": "1"}) as mock_post, \
             patch("backend.cli._poll", return_value={"ok": True}) as mock_poll, \
             patch("sys.stdout", new=io.StringIO()):
            cli.main()
        mock_post.assert_called_once()
        payload = mock_post.call_args[0][2]
        self.assertEqual(payload["inventory_filter"], inv)
        mock_poll.assert_called_once()

    def test_generate_with_out_dir(self):
        argv = [
            "cli",
            "--token",
            "tok",
            "generate",
            "hi",
            "--out-dir",
            "out",
        ]
        result = {"png_url": "/static/a/preview.png", "ldr_url": None, "gltf_url": None}
        with patch.object(sys, "argv", argv), \
             patch("backend.cli._post", return_value={"job_id": "1"}) as mock_post, \
             patch("backend.cli._poll", return_value=result) as mock_poll, \
             patch("backend.cli.request.urlopen") as mock_urlopen, \
             patch("sys.stdout", new=io.StringIO()):
            mock_urlopen.return_value.__enter__.return_value.read.return_value = b"data"
            cli.main()
        mock_post.assert_called_once()
        mock_poll.assert_called_once()
        mock_urlopen.assert_called_once()

    def test_detect_command(self):
        argv = ["cli", "--token", "tok", "detect", "img.png"]
        with patch.object(sys, "argv", argv), \
             patch("backend.cli.open", mock_open(read_data=b"img"), create=True), \
             patch("backend.cli._post", return_value={"job_id": "1"}) as mock_post, \
             patch("backend.cli._poll", return_value={"ok": True}) as mock_poll, \
             patch("sys.stdout", new=io.StringIO()):
            cli.main()
        mock_post.assert_called_once()
        mock_poll.assert_called_once()

    def test_generate_batch_file(self):
        argv = ["cli", "--token", "tok", "generate", "--file", "prompts.txt"]
        prompts = "one\ntwo\n"
        with patch.object(sys, "argv", argv), \
             patch("backend.cli.open", mock_open(read_data=prompts), create=True), \
             patch("backend.cli._post", return_value={"job_id": "1"}) as mock_post, \
             patch("backend.cli._poll", return_value={"ok": True}) as mock_poll, \
             patch("sys.stdout", new=io.StringIO()):
            cli.main()
        self.assertEqual(mock_post.call_count, 2)
        self.assertEqual(mock_poll.call_count, 2)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
