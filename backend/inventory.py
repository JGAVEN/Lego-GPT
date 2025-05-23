"""Utilities for filtering generated bricks by available inventory."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict

_DEFAULT_PATH = Path(__file__).with_name("inventory.json")


def load_inventory(path: str | Path | None = None) -> Dict[str, int]:
    """Load a brick inventory mapping part IDs to counts."""
    p = Path(path) if path else _DEFAULT_PATH
    if not p.exists():
        return {}
    try:
        with open(p) as f:
            data = json.load(f)
            return {str(k): int(v) for k, v in data.items()}
    except Exception:
        return {}


_INVENTORY: Dict[str, int] | None = None


def get_inventory() -> Dict[str, int]:
    """Return the cached inventory, loading it on first use."""
    global _INVENTORY
    if _INVENTORY is None:
        env_path = os.getenv("BRICK_INVENTORY")
        _INVENTORY = load_inventory(env_path)
    return _INVENTORY


def filter_counts(counts: Dict[str, int]) -> Dict[str, int]:
    """Trim brick counts to the available inventory."""
    inv = get_inventory()
    if not inv:
        return counts
    filtered: Dict[str, int] = {}
    for part, qty in counts.items():
        available = inv.get(part, 0)
        if available > 0:
            if qty > available:
                filtered[part] = available
            else:
                filtered[part] = qty
    return filtered

