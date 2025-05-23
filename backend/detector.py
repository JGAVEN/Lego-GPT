"""Stub brick inventory detector.

This module simulates a photo-based brick detector. The real
implementation will run a YOLOv8 model but for the purposes of
testing we simply decode the input and return a fixed inventory map.
"""
from __future__ import annotations

import base64
from typing import Dict


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
        try:
            base64.b64decode(image_data)
        except Exception:
            pass
    # TODO: integrate real YOLOv8 detection here
    return {"3001.DAT": 1}
