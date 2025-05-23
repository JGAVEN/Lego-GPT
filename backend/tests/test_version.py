import sys
import unittest
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import backend  # noqa: E402


class VersionTests(unittest.TestCase):
    def test_version_format(self):
        self.assertRegex(backend.__version__, r"\d+\.\d+\.\d+")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
