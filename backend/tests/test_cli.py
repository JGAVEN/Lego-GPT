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

import backend
import backend.server as server


class CLITests(unittest.TestCase):
    def test_version_flag(self):
        with patch.object(sys, 'argv', ['server', '--version']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                server.main()
                self.assertEqual(fake_out.getvalue().strip(), backend.__version__)

    def test_cli_options_parsed(self):
        argv = [
            'server',
            '--host', '1.2.3.4',
            '--port', '1234',
            '--queue', 'testq',
            '--redis-url', 'redis://host:9999/1',
            '--jwt-secret', 'tok',
            '--rate-limit', '7',
            '--static-root', '/tmp/out',
            '--log-level', 'INFO',
            '--log-file', '/tmp/api.log',
            '--cors-origins', 'http://x',
        ]
        with patch.object(sys, 'argv', argv):
            with patch('backend.server.run') as mock_run:
                server.main()
                mock_run.assert_called_once_with(
                    '1.2.3.4',
                    1234,
                    'testq',
                    'redis://host:9999/1',
                    'tok',
                    7,
                    '/tmp/out',
                    'INFO',
                    '/tmp/api.log',
                    'http://x',
                )


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
