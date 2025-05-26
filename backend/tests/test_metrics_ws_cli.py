import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
import asyncio

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import backend
import backend.metrics_ws as metrics


class MetricsCLITests(unittest.TestCase):
    def test_version_flag(self):
        with patch.object(sys, "argv", ["metrics", "--version"]), patch("sys.stdout", new=io.StringIO()) as out:
            metrics.main()
            self.assertEqual(out.getvalue().strip(), backend.__version__)

    def test_missing_websockets(self):
        with patch.object(metrics, "websockets", None):
            with self.assertRaises(RuntimeError):
                asyncio.run(metrics.run_server("127.0.0.1", 0))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
