import importlib
import os
import sys
import unittest
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


class QueueNameEnvTests(unittest.TestCase):
    def test_env_overrides_queue_name(self):
        os.environ["QUEUE_NAME"] = "testq"
        import backend.worker as worker

        importlib.reload(worker)
        self.assertEqual(worker.QUEUE_NAME, "testq")
        del os.environ["QUEUE_NAME"]
        importlib.reload(worker)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

