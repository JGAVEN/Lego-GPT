from __future__ import annotations

import json
import os
from pathlib import Path


def apply_yaml_config(path: str) -> None:
    """Load key/value pairs from a YAML file into ``os.environ``.

    If ``PyYAML`` is not installed or the file cannot be read, a message is
    printed and the configuration is ignored.
    """
    try:
        import yaml  # type: ignore
    except Exception:
        print("PyYAML not installed; skipping config file", file=os.sys.stderr)
        return

    try:
        data = yaml.safe_load(Path(path).read_text()) or {}
    except Exception as exc:  # pragma: no cover - invalid file
        print(f"Failed to load config {path}: {exc}", file=os.sys.stderr)
        return

    if not isinstance(data, dict):
        print(f"Config {path} must be a mapping", file=os.sys.stderr)
        return

    for key, value in data.items():
        if isinstance(value, (dict, list)):
            os.environ.setdefault(key, json.dumps(value))
        else:
            os.environ.setdefault(key, str(value))
