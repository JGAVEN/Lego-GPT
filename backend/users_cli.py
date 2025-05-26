"""Command-line interface for user management."""

import argparse
from pathlib import Path

import argparse
from pathlib import Path

from backend import HISTORY_ROOT, PREFERENCES_ROOT


def list_users(history_root: Path, preferences_root: Path) -> list[str]:
    users = set()
    if history_root.is_dir():
        for p in history_root.glob("*.jsonl"):
            users.add(p.stem)
    if preferences_root.is_dir():
        for p in preferences_root.glob("*.json"):
            users.add(p.stem)
    return sorted(users)


def delete_user(user: str, history_root: Path, preferences_root: Path) -> None:
    (history_root / f"{user}.jsonl").unlink(missing_ok=True)
    (preferences_root / f"{user}.json").unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Manage Lego GPT users")
    sub = parser.add_subparsers(dest="cmd", required=True)

    ls = sub.add_parser("list", help="List user IDs")
    ls.add_argument(
        "--history-root",
        default=str(HISTORY_ROOT),
        help="History directory (default: env HISTORY_ROOT)",
    )
    ls.add_argument(
        "--preferences-root",
        default=str(PREFERENCES_ROOT),
        help="Preferences directory (default: env PREFERENCES_ROOT)",
    )

    rm = sub.add_parser("delete", help="Delete user data")
    rm.add_argument("user", help="User ID to delete")
    rm.add_argument("--history-root", default=str(HISTORY_ROOT))
    rm.add_argument("--preferences-root", default=str(PREFERENCES_ROOT))

    args = parser.parse_args(argv)
    hist = Path(getattr(args, "history_root"))
    prefs = Path(getattr(args, "preferences_root"))

    if args.cmd == "list":
        for u in list_users(hist, prefs):
            print(u)
    elif args.cmd == "delete":
        delete_user(args.user, hist, prefs)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
