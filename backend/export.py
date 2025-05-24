"""LDraw to glTF export helpers and CLI."""
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


def main(argv: list[str] | None = None) -> None:
    """Command-line interface for ``lego-gpt-export``."""
    import argparse

    parser = argparse.ArgumentParser(description="Convert .ldr model to glTF")
    parser.add_argument("ldr", help="Input .ldr file")
    parser.add_argument("gltf", help="Output .gltf file")
    args = parser.parse_args(argv)
    ldr_to_gltf(args.ldr, args.gltf)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()

