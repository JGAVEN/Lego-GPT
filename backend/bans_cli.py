import argparse
import json
import os
from pathlib import Path
from urllib import request

from backend import BANS_FILE


def _get(url: str, token: str) -> dict:
    req = request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with request.urlopen(req) as resp:
        return json.load(resp)


def _post(url: str, token: str, payload: dict) -> dict:
    data = json.dumps(payload).encode()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    req = request.Request(url, data=data, headers=headers)
    with request.urlopen(req) as resp:
        return json.load(resp)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Sync banned user list")
    parser.add_argument("remote", help="Remote base URL")
    parser.add_argument("--token", default=os.getenv("JWT"), help="Admin JWT token")
    parser.add_argument("--push", action="store_true", help="Push local bans to remote")
    parser.add_argument("--file", default=str(BANS_FILE), help="Path to local bans file")
    args = parser.parse_args(argv)
    path = Path(args.file)
    local = []
    if path.is_file():
        try:
            local = json.loads(path.read_text())
        except Exception:
            local = []
    if args.push:
        _post(f"{args.remote}/bans", args.token, {"bans": local})
        print(f"Pushed {len(local)} bans")
    else:
        data = _get(f"{args.remote}/bans", args.token)
        merged = sorted(set(local) | set(data.get("bans", [])))
        path.write_text(json.dumps(merged, indent=2))
        print(f"Pulled {len(merged)} bans")


if __name__ == "__main__":  # pragma: no cover
    main()
