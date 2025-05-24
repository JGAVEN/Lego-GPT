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
import backend.worker as worker
import detector.worker as detect_worker


class WorkerCLITests(unittest.TestCase):
    def test_worker_version_flag(self):
        with patch.object(sys, 'argv', ['worker', '--version']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                worker.main()
                self.assertEqual(fake_out.getvalue().strip(), backend.__version__)

    def test_worker_options_parsed(self):
        argv = [
            'worker',
            '--redis-url', 'redis://host:9999/1',
            '--queue', 'testq',
        ]
        with patch.object(sys, 'argv', argv):
            with patch('backend.worker.run_worker') as mock_run:
                worker.main()
                mock_run.assert_called_once_with('redis://host:9999/1', 'testq')

    def test_detector_worker_version_flag(self):
        with patch.object(sys, 'argv', ['detector-worker', '--version']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                detect_worker.main()
                self.assertEqual(fake_out.getvalue().strip(), backend.__version__)

    def test_detector_worker_options_parsed(self):
        argv = [
            'detector-worker',
            '--redis-url', 'redis://host:9999/1',
            '--queue', 'detq',
        ]
        with patch.object(sys, 'argv', argv):
            with patch('detector.worker.run_detector') as mock_run:
                detect_worker.main()
                mock_run.assert_called_once_with('redis://host:9999/1', 'detq')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
