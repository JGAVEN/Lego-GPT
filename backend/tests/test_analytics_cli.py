import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

project_root = Path(__file__).resolve().parents[2]
vendor_root = project_root / "vendor"
for p in (project_root, vendor_root):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import backend.analytics_cli as cli


class AnalyticsCLITests(unittest.TestCase):
    def test_push_url(self):
        argv = ["analytics", "-", "--token", "tok", "--push-url", "http://wh"]
        data = {"history": {}}
        with patch.object(sys, "argv", argv), \
             patch("backend.analytics_cli._fetch_metrics", return_value=data), \
             patch("backend.analytics_cli.request.urlopen") as mock_urlopen, \
             patch("sys.stdout", new=io.StringIO()):
            cli.main()
        req = mock_urlopen.call_args[0][0]
        assert req.full_url == "http://wh"
        assert req.headers["Authorization"] == "Bearer tok"
        assert req.headers["Content-type"] == "text/csv"


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
