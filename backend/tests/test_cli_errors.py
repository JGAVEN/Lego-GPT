import io
import unittest
from urllib.error import HTTPError

from pathlib import Path
import sys

project_root = Path(__file__).resolve().parents[2]
vendor_root = project_root / "vendor"
for p in (project_root, vendor_root):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import backend.cli as cli


class CLIErrorTests(unittest.TestCase):
    def test_post_error_message(self):
        err = HTTPError(
            "http://x", 400, "Bad", {}, io.BytesIO(b'{"detail":"oops"}')
        )
        with unittest.mock.patch("backend.cli.request.urlopen", side_effect=err):
            with self.assertRaises(RuntimeError) as cm:
                cli._post("http://x", "tok", {"a": 1})
        self.assertIn("oops", str(cm.exception))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
