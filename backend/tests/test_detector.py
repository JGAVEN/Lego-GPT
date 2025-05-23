import os
import sys
import unittest
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


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
