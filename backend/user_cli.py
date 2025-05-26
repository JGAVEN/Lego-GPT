"""CLI to manage user accounts."""
from __future__ import annotations

import argparse
import os
from pathlib import Path

from backend import HISTORY_ROOT, PREFERENCES_ROOT


def list_users(history: Path, prefs: Path) -> list[str]:
    """Return sorted list of known user IDs."""
    users: set[str] = set()
    if history.is_dir():
        for p in history.glob("*.jsonl"):
            users.add(p.stem)
    if prefs.is_dir():
        for p in prefs.glob("*.json"):
            users.add(p.stem)
    return sorted(users)


def delete_user(user: str, history: Path, prefs: Path) -> None:
    """Remove all data for ``user``."""
    hist_file = history / f"{user}.jsonl"
    pref_file = prefs / f"{user}.json"
    if hist_file.is_file():
        hist_file.unlink()
    if pref_file.is_file():
        pref_file.unlink()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Manage user accounts")
    parser.add_argument(
        "--history",
        default=os.getenv("HISTORY_ROOT", str(HISTORY_ROOT)),
        help="Directory with build history files",
    )
    parser.add_argument(
        "--prefs",
        default=os.getenv("PREFERENCES_ROOT", str(PREFERENCES_ROOT)),
        help="Directory with preference files",
    )
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("list", help="List known users")
    del_p = sub.add_parser("delete", help="Delete a user")
    del_p.add_argument("user", help="User ID")
    args = parser.parse_args(argv)

    history = Path(args.history)
    prefs = Path(args.prefs)
    if args.cmd == "list":
        for u in list_users(history, prefs):
            print(u)
    elif args.cmd == "delete":
        delete_user(args.user, history, prefs)
    else:
        parser.print_help()


if __name__ == "__main__":  # pragma: no cover
    main()
