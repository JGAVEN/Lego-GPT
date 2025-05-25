"""Simple build history log."""
from __future__ import annotations

import json
from typing import Any, Dict

from backend import HISTORY_ROOT

HISTORY_FILE = HISTORY_ROOT / "history.json"


def record(entry: Dict[str, Any]) -> None:
    """Append a build entry to the history file."""
    HISTORY_ROOT.mkdir(parents=True, exist_ok=True)
    try:
        data = json.loads(HISTORY_FILE.read_text()) if HISTORY_FILE.is_file() else []
    except Exception:
        data = []
    data.append(entry)
    HISTORY_FILE.write_text(json.dumps(data, indent=2))


def load() -> list[Dict[str, Any]]:
    """Return the build history list."""
    try:
        return json.loads(HISTORY_FILE.read_text()) if HISTORY_FILE.is_file() else []
    except Exception:
        return []
