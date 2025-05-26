import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import backend.config_gen_cli as config_cli


class ConfigGenCLITests(unittest.TestCase):
    def test_stdout(self):
        argv = ["config"]
        with patch.object(sys, "argv", argv), patch("sys.stdout", new=io.StringIO()) as out:
            config_cli.main()
            text = out.getvalue()
        self.assertIn("JWT_SECRET", text)

    def test_file_output(self):
        tmp = Path("test.yaml")
        argv = ["config", str(tmp)]
        with patch.object(sys, "argv", argv):
            config_cli.main()
        self.assertTrue(tmp.is_file())
        self.assertIn("REDIS_URL", tmp.read_text())
        tmp.unlink()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
