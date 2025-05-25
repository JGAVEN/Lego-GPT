import os
import unittest
from unittest.mock import patch, MagicMock

import importlib


class NotifyTests(unittest.TestCase):
    def test_send_comment_notification(self):
        os.environ["SMTP_HOST"] = "localhost"
        os.environ["COMMENT_NOTIFY_EMAIL"] = "admin@example.com"
        import backend.notify as notify

        importlib.reload(notify)

        with patch("smtplib.SMTP") as mock_smtp:
            smtp_inst = mock_smtp.return_value.__enter__.return_value
            notify.send_comment_notification("1", "u", "hi")
            smtp_inst.send_message.assert_called_once()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
