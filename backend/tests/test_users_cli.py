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
            (hist / "alice.jsonl").write_text("{}\n")
            (prefs / "bob.json").write_text("{}")
            with patch.object(users_cli, "HISTORY_ROOT", hist), \
                 patch.object(users_cli, "PREFERENCES_ROOT", prefs):
                with patch("sys.stdout", new=io.StringIO()) as out:
                    users_cli.main(["list"])
                    data = out.getvalue().splitlines()
                self.assertEqual(sorted(data), ["alice", "bob"])
                users_cli.main(["delete", "alice"])
                self.assertFalse((hist / "alice.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
