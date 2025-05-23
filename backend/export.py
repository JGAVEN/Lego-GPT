"""Stub for converting LDraw files to glTF for AR Quick-Look."""
from __future__ import annotations

import json
from pathlib import Path


def ldr_to_gltf(ldr_path: str | Path, gltf_path: str | Path) -> None:
    """Create a minimal glTF file from an LDraw model."""
    gltf_path = Path(gltf_path)
    gltf_data = {
        "asset": {"version": "2.0"},
        "scene": 0,
        "scenes": [{"nodes": []}],
        "nodes": [],
    }
    gltf_path.write_text(json.dumps(gltf_data))

