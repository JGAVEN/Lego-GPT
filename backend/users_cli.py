"""CLI for listing and deleting user data."""
from __future__ import annotations

import argparse


from backend import HISTORY_ROOT, PREFERENCES_ROOT


def list_users() -> list[str]:
    users: set[str] = set()
    for root in (HISTORY_ROOT, PREFERENCES_ROOT):
        if root.is_dir():
            for p in root.iterdir():
                users.add(p.stem)
    return sorted(users)


def delete_user(user: str) -> None:
    for root in (HISTORY_ROOT, PREFERENCES_ROOT):
        for ext in (".jsonl", ".json"):
            path = root / f"{user}{ext}"
            if path.exists():
                path.unlink()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Manage Lego GPT user accounts")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="List user IDs with stored data")
    delete_p = sub.add_parser("delete", help="Delete stored data for a user")
    delete_p.add_argument("user", help="User ID to delete")
    args = parser.parse_args(argv)
    if args.cmd == "list":
        for u in list_users():
            print(u)
    else:
        delete_user(args.user)
        print(f"Deleted {args.user}")


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
