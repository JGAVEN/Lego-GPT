import importlib
import io
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
import unittest

project_root = Path(__file__).resolve().parents[2]
vendor_root = project_root / "vendor"
for p in (project_root, vendor_root):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import backend.cli as cli


class CLIDotEnvTests(unittest.TestCase):
    def test_cli_loads_dotenv(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            env = Path(tmpdir) / ".env"
            env.write_text("API_URL=http://x\nJWT=tok\n")
            cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                importlib.reload(cli)
                argv = ["cli", "generate", "hi"]
                with patch.object(sys, "argv", argv), \
                     patch("backend.cli._post", return_value={"job_id": "1"}) as mock_post, \
                     patch("backend.cli._poll", return_value={"ok": True}), \
                     patch("sys.stdout", new=io.StringIO()):
                    cli.main()
                mock_post.assert_called_once()
                self.assertEqual(mock_post.call_args[0][0], "http://x/generate")
                self.assertEqual(mock_post.call_args[0][1], "tok")
            finally:
                os.chdir(cwd)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

