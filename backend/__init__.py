"""Backend package for Lego GPT."""

from importlib.metadata import PackageNotFoundError, version

try:  # pragma: no cover - during editable installs
    __version__ = version("lego-gpt-backend")
except PackageNotFoundError:  # pragma: no cover - fallback for tests
    __version__ = "0.0.0"

__all__ = ["__version__"]
