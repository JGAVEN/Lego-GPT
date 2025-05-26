import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import backend.storage as storage


class S3UploadTests(unittest.TestCase):
    def test_maybe_upload_assets_uses_s3(self):
        tmp = Path(tempfile.mkdtemp())
        f = tmp / "file.txt"
        f.write_text("x")
        os.environ["S3_BUCKET"] = "b"
        os.environ["S3_URL_PREFIX"] = "http://cdn"
        import importlib
        importlib.reload(storage)
        with patch.object(storage, "boto3") as mock_boto:
            mock_client = MagicMock()
            mock_boto.client.return_value = mock_client
            urls, uploaded = storage.maybe_upload_assets([f])
            self.assertTrue(uploaded)
            mock_client.upload_file.assert_called_once()
            args, kwargs = mock_client.upload_file.call_args
            self.assertIn("ExtraArgs", kwargs)
            self.assertEqual(kwargs["ExtraArgs"].get("ContentEncoding"), "gzip")
            self.assertEqual(urls[0], "http://cdn/" + f"{f.parent.name}/{f.name}")
        del os.environ["S3_BUCKET"]
        del os.environ["S3_URL_PREFIX"]


if __name__ == "__main__":
    unittest.main()
