import importlib
import os
import sys
import tempfile
from pathlib import Path
import unittest

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

class DotEnvTests(unittest.TestCase):
    def test_dotenv_loaded(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            env_file = tmp_path / '.env'
            env_file.write_text('STATIC_URL_PREFIX=/cdn\n')
            cwd = os.getcwd()
            try:
                os.chdir(tmp_path)
                os.environ.pop('STATIC_URL_PREFIX', None)
                import backend
                importlib.reload(backend)
                self.assertEqual(backend.STATIC_URL_PREFIX, '/cdn')
            finally:
                os.chdir(cwd)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
