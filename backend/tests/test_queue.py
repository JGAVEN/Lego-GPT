import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

project_root = Path(__file__).resolve().parents[2]
vendor_root = project_root / "vendor"
for p in (project_root, vendor_root):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
os.environ["PYTHONPATH"] = str(project_root)

try:
    import fakeredis  # type: ignore
except Exception:  # pragma: no cover - optional dep may be missing
    fakeredis = None

from rq import Queue, SimpleWorker
import backend.worker as worker


class QueueTests(unittest.TestCase):
    def test_generate_job_runs(self):
        if fakeredis is None:
            self.skipTest("fakeredis not installed")
        redis_conn = fakeredis.FakeRedis()
        q = Queue(worker.QUEUE_NAME, connection=redis_conn)
        with patch("backend.worker.generate_lego_model") as mock_gen:
            mock_gen.return_value = {
                "png_url": "/static/x/preview.png",
                "ldr_url": None,
                "gltf_url": None,
                "brick_counts": {},
            }
            job = q.enqueue(worker.generate_job, "cube", 1, None)
            SimpleWorker([q], connection=redis_conn).work(burst=True)
            self.assertTrue(job.is_finished)
            self.assertEqual(job.result["png_url"], "/static/x/preview.png")
            mock_gen.assert_called_once_with("cube", 1, None)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
