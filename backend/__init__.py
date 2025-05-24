"""Backend package for Lego GPT."""

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import os

try:  # pragma: no cover - during editable installs
    __version__ = version("lego-gpt-backend")
except PackageNotFoundError:  # pragma: no cover - fallback for tests
    __version__ = "0.0.0"

PACKAGE_DIR = Path(__file__).parent
_env_static = os.getenv("STATIC_ROOT")
STATIC_ROOT = Path(_env_static) if _env_static else PACKAGE_DIR / "static"
STATIC_ROOT = STATIC_ROOT.resolve()

# URL prefix returned for generated assets
STATIC_URL_PREFIX = os.getenv("STATIC_URL_PREFIX", "/static")

__all__ = ["__version__", "STATIC_ROOT", "STATIC_URL_PREFIX"]
