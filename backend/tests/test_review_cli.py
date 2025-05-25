import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import backend.review_cli as review


class ReviewCLITests(unittest.TestCase):
    def test_list_and_approve(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sub_dir = Path(tmpdir) / "subs"
            sub_dir.mkdir()
            ex_file = Path(tmpdir) / "examples.json"
            ex_file.write_text("[]")
            sub_file = sub_dir / "a.json"
            sub_file.write_text(json.dumps({"title": "Cool Castle", "prompt": "build a cool castle"}))

            with unittest.mock.patch.object(sys, "argv", [
                "review", "--submissions", str(sub_dir), "--examples", str(ex_file), "list"
            ]), io.StringIO() as buf, unittest.mock.patch("sys.stdout", buf):
                review.main()
                out = buf.getvalue()
                self.assertIn("a.json", out)

            with unittest.mock.patch.object(sys, "argv", [
                "review", "--submissions", str(sub_dir), "--examples", str(ex_file), "approve", "a.json"
            ]), io.StringIO() as buf, unittest.mock.patch("sys.stdout", buf):
                review.main()

            data = json.loads(ex_file.read_text())
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["title"], "Cool Castle")
            self.assertIn("cool", data[0]["tags"])
            self.assertIn("castle", data[0]["tags"])
            self.assertFalse(sub_file.exists())


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
