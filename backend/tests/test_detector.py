import os
import sys
import unittest
import unittest.mock
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
vendor_root = project_root / "vendor"
for p in (project_root, vendor_root):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
os.environ["PYTHONPATH"] = str(project_root)

from backend.detector import detect_inventory
from backend.worker import detect_job


class DetectorTests(unittest.TestCase):
    def test_detect_inventory_stub(self):
        counts = detect_inventory("YWJj")
        self.assertIsInstance(counts, dict)
        self.assertIn("3001.DAT", counts)

    def test_invalid_base64_raises(self):
        with self.assertRaises(ValueError):
            detect_inventory("@@invalid@@")

    def test_detect_job(self):
        result = detect_job("YWJj")
        self.assertIn("brick_counts", result)
        self.assertIsInstance(result["brick_counts"], dict)

    def test_detect_inventory_cache(self):
        class FakeRedis:
            def __init__(self):
                self.store = {}

            def get(self, key):
                return self.store.get(key)

            def setex(self, key, ttl, value):
                self.store[key] = value

        from backend import detector as det

        fake = FakeRedis()
        with unittest.mock.patch.object(det, "_REDIS", fake):
            counts1 = det.detect_inventory("YWJj")
            self.assertIn("3001.DAT", counts1)
            counts2 = det.detect_inventory("YWJj")
            self.assertEqual(counts1, counts2)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
