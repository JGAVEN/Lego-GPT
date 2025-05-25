"""CLI tool to review community example submissions."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from backend import SUBMISSIONS_ROOT


def list_submissions(path: Path) -> None:
    """Print pending submission files."""
    for item in sorted(path.glob("*.json")):
        try:
            data = json.loads(item.read_text())
            title = data.get("title", "?")
            prompt = data.get("prompt", "")
        except Exception:
            title = "?"
            prompt = ""
        print(f"{item.name}\t{title}\t{prompt}")


def approve_submission(path: Path, file_name: str, examples: Path) -> None:
    """Move submission into the examples list."""
    file_path = path / file_name
    data = json.loads(file_path.read_text())
    examples_data = json.loads(examples.read_text()) if examples.is_file() else []
    next_id = str(int(examples_data[-1]["id"]) + 1) if examples_data else "1"
    entry = {
        "id": next_id,
        "title": data["title"],
        "prompt": data["prompt"],
    }
    if "image" in data:
        entry["image"] = data["image"]
    examples_data.append(entry)
    examples.write_text(json.dumps(examples_data, indent=2))
    file_path.unlink()
    print(f"Approved {file_name} as id {next_id}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Review example submissions")
    parser.add_argument(
        "--submissions",
        default=os.getenv("SUBMISSIONS_ROOT", str(SUBMISSIONS_ROOT)),
        help="Directory with pending submissions",
    )
    parser.add_argument(
        "--examples",
        default=os.getenv(
            "EXAMPLES_FILE",
            str(Path(__file__).resolve().parents[1] / "frontend/public/examples.json"),
        ),
        help="Path to examples.json",
    )
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("list", help="List pending submissions")
    appr = sub.add_parser("approve", help="Approve a submission")
    appr.add_argument("file", help="Submission filename")
    args = parser.parse_args(argv)
    submissions = Path(args.submissions)
    examples = Path(args.examples)
    if args.cmd == "list":
        list_submissions(submissions)
    elif args.cmd == "approve":
        approve_submission(submissions, args.file, examples)
    else:
        parser.print_help()


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
