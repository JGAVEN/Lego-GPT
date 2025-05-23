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

import backend
import backend.server as server


class CLITests(unittest.TestCase):
    def test_version_flag(self):
        with patch.object(sys, 'argv', ['server', '--version']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                server.main()
                self.assertEqual(fake_out.getvalue().strip(), backend.__version__)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
