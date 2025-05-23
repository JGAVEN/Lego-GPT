import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

project_root = Path(__file__).resolve().parents[2]
for p in (project_root, project_root / "vendor"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import detector.train as train  # noqa: E402


class TrainScriptTests(unittest.TestCase):
    def test_main_with_stub(self):
        class FakeYOLO:
            def __init__(self, *args, **kwargs):
                pass

            def train(self, data=None, epochs=0):
                class R:
                    save_dir = "/tmp"
                return R()

        with patch.dict("sys.modules", {"ultralytics": SimpleNamespace(YOLO=FakeYOLO)}):
            with patch.object(Path, "rename") as mock_rename:
                train.main(["data.yaml", "--epochs", "1", "--out", "model.pt"])
                mock_rename.assert_called_once()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
