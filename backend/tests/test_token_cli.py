import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import backend
import backend.token_cli as token_cli


class TokenCLITests(unittest.TestCase):
    def test_generate_token_cli(self):
        argv = ["token", "--secret", "s3", "--sub", "alice", "--exp", "60", "--role", "admin"]
        with patch.object(sys, "argv", argv), patch("sys.stdout", new=io.StringIO()) as fake_out:
            token_cli.main()
            token = fake_out.getvalue().strip()
        payload = backend.auth.decode(token, "s3")
        self.assertEqual(payload["sub"], "alice")
        self.assertEqual(payload["role"], "admin")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
