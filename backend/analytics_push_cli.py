"""CLI to push analytics metrics to a remote server."""
from __future__ import annotations

import argparse
import json
import os
from urllib import request
from urllib.error import HTTPError

from backend.analytics_cli import _fetch_metrics


def _post(url: str, payload: dict) -> None:
    data = json.dumps(payload).encode()
    req = request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with request.urlopen(req):
        pass


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Push metrics snapshot to remote")
    parser.add_argument("dest", help="Destination URL")
    parser.add_argument("--url", default=os.getenv("API_URL", "http://localhost:8000"))
    parser.add_argument("--token", default=os.getenv("JWT"))
    args = parser.parse_args(argv)
    if not args.token:
        parser.error("Admin token required")
    try:
        data = _fetch_metrics(args.url, args.token)
    except HTTPError as exc:
        raise SystemExit(f"Failed to fetch metrics: {exc}")
    try:
        _post(args.dest, data)
    except HTTPError as exc:
        raise SystemExit(f"Failed to push metrics: {exc}")


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
