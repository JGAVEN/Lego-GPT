import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import backend.analytics_cli as analytics_cli


class AnalyticsCLITests(unittest.TestCase):
    def test_export_and_push(self):
        data = {
            "history": {"req": {"1": 2}}
        }
        with patch("backend.analytics_cli._fetch_metrics", return_value=data):
            with patch("backend.analytics_cli._push_csv") as push_mock:
                argv = ["analytics", "-", "--token", "t", "--push-url", "http://dst"]
                with patch.object(sys, "argv", argv), patch("sys.stdout", new=io.StringIO()) as out:
                    analytics_cli.main()
                    out_val = out.getvalue().strip()
                self.assertIn("metric,timestamp,value", out_val)
                push_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
