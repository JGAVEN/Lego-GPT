"""Clean up generated static assets."""
from __future__ import annotations

import argparse
import os
import shutil
import time
from pathlib import Path

from backend import STATIC_ROOT


def cleanup(path: Path = STATIC_ROOT, days: int = 7, dry_run: bool = False) -> int:
    """Remove subdirectories in *path* older than *days* days.

    If ``dry_run`` is ``True`` the directories are listed but not removed.

    Returns the number of directories removed (or that would be removed in dry
    run mode).
    """
    threshold = time.time() - days * 86400
    count = 0
    for item in path.iterdir():
        if not item.is_dir():
            continue
        if item.stat().st_mtime < threshold:
            if dry_run:
                print(f"Would remove {item}")
            else:
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
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=os.getenv("CLEANUP_DRY_RUN", "0") not in {"", "0", "false", "False"},
        help="List directories without deleting them (default: env CLEANUP_DRY_RUN)",
    )
    args = parser.parse_args(argv)
    removed = cleanup(Path(args.path), args.days, args.dry_run)
    print(f"Removed {removed} directories")


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
