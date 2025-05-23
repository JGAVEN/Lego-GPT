"""Backend package for Lego GPT."""

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

try:  # pragma: no cover - during editable installs
    __version__ = version("lego-gpt-backend")
except PackageNotFoundError:  # pragma: no cover - fallback for tests
    __version__ = "0.0.0"

PACKAGE_DIR = Path(__file__).parent
STATIC_ROOT = PACKAGE_DIR / "static"

__all__ = ["__version__", "STATIC_ROOT"]
