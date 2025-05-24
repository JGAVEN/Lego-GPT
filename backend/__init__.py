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
    __version__ = "0.5.21"

PACKAGE_DIR = Path(__file__).parent
_env_static = os.getenv("STATIC_ROOT")
STATIC_ROOT = Path(_env_static) if _env_static else PACKAGE_DIR / "static"
STATIC_ROOT = STATIC_ROOT.resolve()

# URL prefix returned for generated assets
STATIC_URL_PREFIX = os.getenv("STATIC_URL_PREFIX", "/static")

__all__ = ["__version__", "STATIC_ROOT", "STATIC_URL_PREFIX"]
