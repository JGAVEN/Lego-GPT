import importlib
import logging
import os
import tempfile
from pathlib import Path
import sys
import unittest

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

class LoggingConfigTests(unittest.TestCase):
    def test_env_var_sets_level(self):
        os.environ['LOG_LEVEL'] = 'WARNING'
        import backend.logging_config as lc
        importlib.reload(lc)
        lc.setup_logging()
        self.assertEqual(logging.getLogger().level, logging.WARNING)

    def test_log_file_env(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "out.log"
            os.environ['LOG_FILE'] = str(path)
            import backend.logging_config as lc
            importlib.reload(lc)
            for h in logging.root.handlers[:]:
                logging.root.removeHandler(h)
            lc.setup_logging()
            logging.info("hi")
            self.assertTrue(path.exists())

