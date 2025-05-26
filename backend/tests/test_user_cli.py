import io
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import backend.user_cli as user_cli


class UserCLITests(unittest.TestCase):
    def test_list_and_delete(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            hist = Path(tmpdir) / "history"
            prefs = Path(tmpdir) / "prefs"
            hist.mkdir()
            prefs.mkdir()
            (hist / "alice.jsonl").write_text("log")
            (prefs / "bob.json").write_text("{}")

            argv = [
                "users",
                "--history",
                str(hist),
                "--prefs",
                str(prefs),
                "list",
            ]
            with mock.patch.object(sys, "argv", argv), io.StringIO() as buf, mock.patch(
                "sys.stdout", buf
            ):
                user_cli.main()
                out = buf.getvalue().splitlines()
            self.assertIn("alice", out)
            self.assertIn("bob", out)

            argv = [
                "users",
                "--history",
                str(hist),
                "--prefs",
                str(prefs),
                "delete",
                "alice",
            ]
            with mock.patch.object(sys, "argv", argv):
                user_cli.main()
            self.assertFalse((hist / "alice.jsonl").exists())


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
