"""Backend package for Lego GPT."""

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import os

# Load environment variables from a `.env` file.
# Prefer ``python-dotenv`` if available, otherwise fall back to a tiny loader.
try:  # pragma: no cover - optional dependency
    from dotenv import load_dotenv

    load_dotenv()
except Exception:  # pragma: no cover - ignore if missing
    env_path = Path(".env")
    if env_path.is_file():
        for line in env_path.read_text().splitlines():
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())

try:  # pragma: no cover - during editable installs
    __version__ = version("lego-gpt-backend")
except PackageNotFoundError:  # pragma: no cover - fallback for tests
    __version__ = "0.5.71"

PACKAGE_DIR = Path(__file__).parent
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
_env_static = os.getenv("STATIC_ROOT")
STATIC_ROOT = Path(_env_static) if _env_static else PACKAGE_DIR / "static"
STATIC_ROOT = STATIC_ROOT.resolve()

# Directory where example submissions are stored for review
_env_sub = os.getenv("SUBMISSIONS_ROOT")
SUBMISSIONS_ROOT = Path(_env_sub) if _env_sub else PACKAGE_DIR / "submissions"
SUBMISSIONS_ROOT = SUBMISSIONS_ROOT.resolve()

# Optional Redis URL to share the moderation queue across instances
SUBMISSIONS_REDIS_URL = os.getenv("SUBMISSIONS_REDIS_URL")

# Directory where example comments are stored
_env_comments = os.getenv("COMMENTS_ROOT")
COMMENTS_ROOT = (
    Path(_env_comments) if _env_comments else PACKAGE_DIR / "comments"
)
COMMENTS_ROOT = COMMENTS_ROOT.resolve()

# Directory where example reports are stored
_env_reports = os.getenv("REPORTS_ROOT")
REPORTS_ROOT = Path(_env_reports) if _env_reports else PACKAGE_DIR / "reports"
REPORTS_ROOT = REPORTS_ROOT.resolve()

# JSON file storing banned user IDs
_env_bans = os.getenv("BANS_FILE")
BANS_FILE = Path(_env_bans) if _env_bans else PACKAGE_DIR / "banned.json"
BANS_FILE = BANS_FILE.resolve()

# Directory storing per-user build history
_env_history = os.getenv("HISTORY_ROOT")
HISTORY_ROOT = Path(_env_history) if _env_history else PACKAGE_DIR / "history"
HISTORY_ROOT = HISTORY_ROOT.resolve()

# Directory storing per-user notification preferences
_env_prefs = os.getenv("PREFERENCES_ROOT")
PREFERENCES_ROOT = Path(_env_prefs) if _env_prefs else PACKAGE_DIR / "preferences"
PREFERENCES_ROOT = PREFERENCES_ROOT.resolve()

# Email notification settings
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "25"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM", "lego-gpt@localhost")
COMMENT_NOTIFY_EMAIL = os.getenv("COMMENT_NOTIFY_EMAIL")

# URL prefix returned for generated assets
STATIC_URL_PREFIX = os.getenv("STATIC_URL_PREFIX", "/static")

__all__ = [
    "__version__",
    "STATIC_ROOT",
    "STATIC_URL_PREFIX",
    "REDIS_URL",
    "SUBMISSIONS_ROOT",
    "SUBMISSIONS_REDIS_URL",
    "COMMENTS_ROOT",
    "REPORTS_ROOT",
    "BANS_FILE",
    "HISTORY_ROOT",
    "PREFERENCES_ROOT",
    "SMTP_HOST",
    "SMTP_PORT",
    "SMTP_USER",
    "SMTP_PASSWORD",
    "SMTP_FROM",
    "COMMENT_NOTIFY_EMAIL",
]
