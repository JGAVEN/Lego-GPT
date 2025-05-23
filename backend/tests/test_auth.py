import sys
import time
import unittest
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend import auth  # noqa: E402


class AuthTests(unittest.TestCase):
    def test_encode_decode_roundtrip(self):
        token = auth.encode({"sub": "alice"}, "s3cret")
        payload = auth.decode(token, "s3cret")
        self.assertEqual(payload["sub"], "alice")

    def test_bad_signature(self):
        token = auth.encode({"sub": "alice"}, "s3cret")
        with self.assertRaises(ValueError):
            auth.decode(token, "wrong")

    def test_expired_token(self):
        past = int(time.time()) - 1
        token = auth.encode({"sub": "alice"}, "s3cret", exp=past)
        with self.assertRaises(ValueError):
            auth.decode(token, "s3cret")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
