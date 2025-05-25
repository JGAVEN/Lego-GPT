import os
import smtplib
from email.message import EmailMessage

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "25"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM", "lego-gpt@localhost")
COMMENT_NOTIFY_EMAIL = os.getenv("COMMENT_NOTIFY_EMAIL")


def send_comment_notification(example_id: str, user: str, text: str) -> None:
    """Send an email when a new comment is posted."""
    host = SMTP_HOST
    to_addr = COMMENT_NOTIFY_EMAIL
    if not host or not to_addr:
        return
    msg = EmailMessage()
    msg["Subject"] = f"New comment on example {example_id}"
    msg["From"] = SMTP_FROM
    msg["To"] = to_addr
    msg.set_content(f"{user} commented:\n\n{text}")
    with smtplib.SMTP(host, SMTP_PORT) as smtp:
        if SMTP_USER:
            try:
                smtp.login(SMTP_USER, SMTP_PASSWORD or "")
            except Exception:
                return
        try:
            smtp.send_message(msg)
        except Exception:
            pass

