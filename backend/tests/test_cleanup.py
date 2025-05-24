import os
import sys
import time
import shutil
import unittest
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend.cleanup import cleanup


class CleanupTests(unittest.TestCase):
    def test_cleanup_removes_old_dirs(self):
        base = Path("test-static")
        base.mkdir(exist_ok=True)
        old_d = base / "old"
        new_d = base / "new"
        old_d.mkdir()
        new_d.mkdir()
        old_time = time.time() - 2 * 86400
        os.utime(old_d, (old_time, old_time))
        removed = cleanup(base, days=1)
        self.assertEqual(removed, 1)
        self.assertFalse(old_d.exists())
        self.assertTrue(new_d.exists())
        shutil.rmtree(base)

    def test_cleanup_dry_run(self):
        base = Path("test-static")
        base.mkdir(exist_ok=True)
        old_d = base / "old"
        old_d.mkdir()
        old_time = time.time() - 2 * 86400
        os.utime(old_d, (old_time, old_time))
        removed = cleanup(base, days=1, dry_run=True)
        self.assertEqual(removed, 1)
        self.assertTrue(old_d.exists())
        shutil.rmtree(base)


if __name__ == "__main__":
    unittest.main()
