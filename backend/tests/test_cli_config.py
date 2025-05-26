import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

project_root = Path(__file__).resolve().parents[2]
vendor_root = project_root / "vendor"
for p in (project_root, vendor_root):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import backend.cli as cli


class CLIConfigTests(unittest.TestCase):
    def test_token_from_config(self):
        argv = ["cli", "generate", "hello"]
        with patch.object(sys, "argv", argv), \
             patch("pathlib.Path.is_file", return_value=True), \
             patch("pathlib.Path.read_text", return_value='{"token":"cfg"}'), \
             patch("backend.cli._post", return_value={"job_id": "1"}), \
             patch("backend.cli._stream_progress"), \
             patch("backend.cli._poll", return_value={"ok": True}), \
             patch("sys.stdout", new=io.StringIO()):
            cli.main()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
