import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# Ensure project root is importable
project_root = Path(__file__).resolve().parents[2]
vendor_root = project_root / "vendor"
for p in (project_root, vendor_root):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
os.environ["PYTHONPATH"] = str(project_root)

from backend.api import generate_lego_model  # noqa: E402


class GenerateTests(unittest.TestCase):
    @patch("backend.api.generate")
    def test_generate_endpoint(self, mock_generate):
        mock_generate.return_value = (
            "backend/static/x/preview.png",
            "backend/static/x/model.ldr",
            "backend/static/x/model.gltf",
            {"Brick": 1},
        )

        inv = {"Brick": 1}
        data = generate_lego_model("blue cube", 42, inv)
        self.assertIn("png_url", data)
        self.assertTrue(data["png_url"].endswith("preview.png"))
        self.assertIn("ldr_url", data)
        self.assertTrue(data["ldr_url"].endswith("model.ldr"))
        self.assertTrue(data["gltf_url"].endswith("model.gltf"))
        mock_generate.assert_called_once_with("blue cube", 42, inv)
        self.assertIsInstance(data["brick_counts"], dict)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
