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


def ldr_to_pdf(ldr_path: str | Path, pdf_path: str | Path) -> None:
    """Create a tiny placeholder PDF without external dependencies."""
    content = (
        b"%PDF-1.4\n"
        b"1 0 obj<<>>endobj\n"
        b"2 0 obj<<>>endobj\n"
        b"trailer<<>>\nstartxref\n9\n%%EOF"
    )
    Path(pdf_path).write_bytes(content)


def main(argv: list[str] | None = None) -> None:
    """Command-line interface for ``lego-gpt-export``."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert .ldr model to glTF and/or PDF instructions"
    )
    parser.add_argument("ldr", help="Input .ldr file")
    parser.add_argument("gltf", help="Output .gltf file")
    parser.add_argument("--pdf", help="Output PDF instructions")
    args = parser.parse_args(argv)
    ldr_to_gltf(args.ldr, args.gltf)
    if args.pdf:
        ldr_to_pdf(args.ldr, args.pdf)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()

