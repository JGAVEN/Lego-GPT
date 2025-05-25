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
    """Create a minimal multi-page PDF listing parts used."""
    ldr_path = Path(ldr_path)
    parts: dict[str, int] = {}
    for line in ldr_path.read_text().splitlines():
        if line.startswith("1 "):
            part = line.split()[1]
            parts[part] = parts.get(part, 0) + 1

    header = b"%PDF-1.4\n"
    objects = []
    pages = []

    def add_obj(data: bytes) -> int:
        idx = len(objects) + 1
        objects.append(data)
        return idx

    page_content = "Parts list:\n" + "\n".join(
        f"{p}: {c}" for p, c in sorted(parts.items())
    )
    stream = f"BT /F1 12 Tf 50 750 Td ({page_content}) Tj ET".encode()
    contents_id = add_obj(b"<<>>stream\n" + stream + b"\nendstream")
    page_id = add_obj(
        f"<< /Type /Page /Parent 3 0 R /Contents {contents_id} 0 R >>".encode()
    )
    pages.append(page_id)

    pages_str = (
        "<< /Type /Pages /Kids ["
        + " ".join(f"{p} 0 R" for p in pages)
        + " ] /Count "
        + str(len(pages))
        + " >>"
    )
    pages_id = add_obj(pages_str.encode())
    catalog_id = add_obj(f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode())

    xref_offset = len(header)
    body = b""
    offsets = []
    for obj_id, obj in enumerate(objects, 1):
        offsets.append(xref_offset + len(body))
        body += f"{obj_id} 0 obj\n".encode() + obj + b"\nendobj\n"

    xref = b"xref\n0 " + str(len(objects) + 1).encode() + b"\n0000000000 65535 f \n"
    for off in offsets:
        xref += f"{off:010d} 00000 n \n".encode()
    trailer = (
        b"trailer<<" +
        f"/Root {catalog_id} 0 R /Size {len(objects)+1}".encode() +
        b">>\nstartxref\n" +
        str(xref_offset + len(body)).encode() + b"\n%%EOF"
    )
    pdf = header + body + xref + trailer
    Path(pdf_path).write_bytes(pdf)


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

