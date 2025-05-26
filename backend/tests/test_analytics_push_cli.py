import sys
from pathlib import Path
from unittest.mock import patch
import unittest

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import backend.analytics_push_cli as push_cli


class AnalyticsPushCLITests(unittest.TestCase):
    def test_push_cli(self):
        with patch.object(push_cli, "_fetch_metrics", return_value={"m": 1}) as fm, \
             patch.object(push_cli, "_post") as mp:
            with patch.object(sys, "argv", ["push", "http://dest", "--token", "t"]):
                push_cli.main()
            fm.assert_called_once()
            mp.assert_called_once_with("http://dest", {"m": 1})


if __name__ == "__main__":
    unittest.main()
