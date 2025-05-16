import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ensure the project root is first in sys.path so "from backend.api import app" works
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
os.environ["PYTHONPATH"] = str(project_root)

from fastapi.testclient import TestClient
from backend.api import app

client = TestClient(app)

@patch("backend.inference.load_model")
def test_generate_endpoint(mock_load_model):
    mock_model = MagicMock()
    mock_model.generate.return_value = {
        "png": b"fake_png_data",
        "ldr": "0 FAKE_BRICK 0 0 0",
        "brick_counts": {"Brick": 1}
    }
    mock_load_model.return_value = mock_model

    response = client.post("/generate", json={"prompt": "blue cube", "seed": 42})
    assert response.status_code == 200

    data = response.json()
    assert "png_url" in data and data["png_url"].endswith("preview.png")
    assert "ldr_url" in data and data["ldr_url"].endswith("model.ldr")
    assert isinstance(data["brick_counts"], dict)
