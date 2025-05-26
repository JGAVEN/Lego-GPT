import io
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
import unittest

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import backend.users_cli as users_cli


class UsersCLITests(unittest.TestCase):
    def test_list_and_delete(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            hist = Path(tmpdir) / "history"
            prefs = Path(tmpdir) / "prefs"
            hist.mkdir()
            prefs.mkdir()
            (hist / "alice.jsonl").write_text("")
            (prefs / "bob.json").write_text("{}")
            argv = ["users", "list", "--history-root", str(hist), "--preferences-root", str(prefs)]
            with patch.object(sys, "argv", argv), patch("sys.stdout", new=io.StringIO()) as out:
                users_cli.main()
                result = set(out.getvalue().strip().splitlines())
            self.assertEqual(result, {"alice", "bob"})
            argv = ["users", "delete", "alice", "--history-root", str(hist), "--preferences-root", str(prefs)]
            with patch.object(sys, "argv", argv):
                users_cli.main()
            self.assertFalse((hist / "alice.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
