import logging
import os


def setup_logging(level: str | None = None, log_file: str | None = None) -> None:
    """Configure basic logging for the application.

    Parameters
    ----------
    level:
        Logging level name (e.g. ``"INFO"``). Defaults to the ``LOG_LEVEL``
        environment variable or ``INFO``.
    log_file:
        Optional path to a file to write logs to. Defaults to ``LOG_FILE`` env
        var if not provided.
    """

    lvl = (level or os.getenv("LOG_LEVEL", "INFO")).upper()
    if not hasattr(logging, lvl):
        lvl = "INFO"
    log_path = log_file or os.getenv("LOG_FILE") or None
    logging.basicConfig(level=getattr(logging, lvl), filename=log_path)
