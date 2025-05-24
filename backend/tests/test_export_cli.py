import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
import unittest

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import backend.export as export


class ExportCLITests(unittest.TestCase):
    def test_export_cli(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            ldr = Path(tmpdir) / "m.ldr"
            gltf = Path(tmpdir) / "m.gltf"
            ldr.write_text("0 FILE m.ldr")
            argv = ["export", str(ldr), str(gltf)]
            with patch.object(sys, "argv", argv):
                export.main()
            self.assertTrue(gltf.exists())


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
