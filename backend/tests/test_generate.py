import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Ensure project root is importable
project_root = Path(__file__).resolve().parents[2]
vendor_root = project_root / "vendor"
for p in (project_root, vendor_root):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
os.environ["PYTHONPATH"] = str(project_root)

from backend.api import generate_lego_model  # noqa: E402


class GenerateTests(unittest.TestCase):
    @patch("backend.inference.ldr_to_gltf")
    @patch("backend.inference.load_model")
    def test_generate_endpoint(self, mock_load_model, mock_gltf):
        mock_model = MagicMock()
        mock_model.generate.return_value = {
            "png": b"fake_png_data",
            "ldr": "0 FAKE_BRICK 0 0 0",
            "brick_counts": {"Brick": 1}
        }
        mock_load_model.return_value = mock_model

        data = generate_lego_model("blue cube", 42)
        self.assertIn("png_url", data)
        self.assertTrue(data["png_url"].endswith("preview.png"))
        self.assertIn("ldr_url", data)
        self.assertTrue(data["ldr_url"].endswith("model.ldr"))
        self.assertTrue(data["gltf_url"].endswith("model.gltf"))
        mock_gltf.assert_called_once()
        self.assertIsInstance(data["brick_counts"], dict)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
