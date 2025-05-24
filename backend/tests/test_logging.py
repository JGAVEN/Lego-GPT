import importlib
import logging
import os
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

