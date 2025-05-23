"""Stub brick inventory detector.

This module simulates a photo-based brick detector. The real
implementation will run a YOLOv8 model but for the purposes of
testing we simply decode the input and return a fixed inventory map.
"""
from __future__ import annotations

import base64
from typing import Dict


def _validate_base64(data: str) -> None:
    """Ensure *data* is valid base64 or raise ``ValueError``."""
    try:
        base64.b64decode(data, validate=True)
    except Exception as exc:  # pragma: no cover - sanity check
        raise ValueError("invalid base64 image data") from exc


def detect_inventory(image_data: bytes | str) -> Dict[str, int]:
    """Return a fake brick inventory map from a photo.

    Parameters
    ----------
    image_data : bytes | str
        Raw bytes or base64-encoded image data. The current
        implementation ignores the content and returns a constant
        dictionary for tests.
    """
    if isinstance(image_data, str):
        _validate_base64(image_data)
    else:
        image_data = base64.b64encode(image_data).decode()
        _validate_base64(image_data)
    # TODO: integrate real YOLOv8 detection here
    return {"3001.DAT": 1}
