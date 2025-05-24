import importlib
import os
import sys
import unittest
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

class StaticRootEnvTests(unittest.TestCase):
    def test_env_overrides_default(self):
        tmp_dir = Path("/tmp/legogpt-test-static")
        os.environ["STATIC_ROOT"] = str(tmp_dir)
        import backend
        importlib.reload(backend)
        self.assertEqual(backend.STATIC_ROOT, tmp_dir.resolve())
        del os.environ["STATIC_ROOT"]
        importlib.reload(backend)

if __name__ == "__main__":
    unittest.main()
