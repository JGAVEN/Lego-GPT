import logging
import os


def setup_logging(level: str | None = None) -> None:
    """Configure basic logging for the application."""
    lvl = (level or os.getenv("LOG_LEVEL", "INFO")).upper()
    if not hasattr(logging, lvl):
        lvl = "INFO"
    logging.basicConfig(level=getattr(logging, lvl))
