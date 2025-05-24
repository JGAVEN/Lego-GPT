"""Clean up generated static assets."""
from __future__ import annotations

import argparse
import os
import shutil
import time
from pathlib import Path

from backend import STATIC_ROOT


def cleanup(path: Path = STATIC_ROOT, days: int = 7) -> int:
    """Remove subdirectories in *path* older than *days* days.

    Returns the number of directories removed.
    """
    threshold = time.time() - days * 86400
    count = 0
    for item in path.iterdir():
        if not item.is_dir():
            continue
        if item.stat().st_mtime < threshold:
            shutil.rmtree(item, ignore_errors=True)
            count += 1
    return count


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Remove old generated assets")
    parser.add_argument(
        "--path",
        default=os.getenv("STATIC_ROOT", str(STATIC_ROOT)),
        help="Directory containing generated assets",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=int(os.getenv("CLEANUP_DAYS", "7")),
        help="Delete files older than this many days (default: env CLEANUP_DAYS or 7)",
    )
    args = parser.parse_args(argv)
    removed = cleanup(Path(args.path), args.days)
    print(f"Removed {removed} directories")


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
