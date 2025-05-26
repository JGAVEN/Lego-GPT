"""CLI to import or export community examples."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def export_examples(src: Path) -> str:
    data = json.loads(src.read_text()) if src.is_file() else []
    return json.dumps(data, indent=2)


def import_examples(src: Path, dest: Path) -> None:
    data = json.loads(src.read_text()) if src.is_file() else []
    dest.write_text(json.dumps(data, indent=2))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Export or import examples")
    parser.add_argument("command", choices=["export", "import"])
    parser.add_argument("file", help="Input or output file ('-' for stdout)")
    parser.add_argument(
        "--examples",
        default=str(Path(__file__).resolve().parents[1] / "frontend/public/examples.json"),
        help="Path to examples.json",
    )
    args = parser.parse_args(argv)
    examples = Path(args.examples)
    path = Path(args.file)
    if args.command == "export":
        data = export_examples(examples)
        if args.file == "-":
            print(data)
        else:
            path.write_text(data)
    else:
        import_examples(path, examples)


if __name__ == "__main__":  # pragma: no cover
    main()

