"""CLI to export analytics metrics history to CSV."""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from urllib import request
from urllib.error import HTTPError


def _fetch_metrics(url: str, token: str) -> dict:
    req = request.Request(f"{url}/metrics", headers={"Authorization": f"Bearer {token}"})
    with request.urlopen(req) as resp:
        return json.load(resp)


def export_csv(data: dict) -> str:
    lines = ["metric,timestamp,value"]
    history = data.get("history", {})
    for metric, buckets in history.items():
        for ts, val in buckets.items():
            dt = datetime.utcfromtimestamp(int(ts) * 60).isoformat()
            lines.append(f"{metric},{dt},{val}")
    return "\n".join(lines) + "\n"


def _push_metrics(csv_data: str, url: str, token: str) -> None:
    req = request.Request(
        url,
        data=csv_data.encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "text/csv",
        },
    )
    with request.urlopen(req):
        pass


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Export metrics history to CSV")
    parser.add_argument("file", help="Output CSV file ('-' for stdout)")
    parser.add_argument("--url", default=os.getenv("API_URL", "http://localhost:8000"))
    parser.add_argument("--token", default=os.getenv("JWT"))
    parser.add_argument("--push-url", default=os.getenv("WAREHOUSE_URL"))
    args = parser.parse_args(argv)
    if not args.token:
        parser.error("Admin token required")
    try:
        data = _fetch_metrics(args.url, args.token)
    except HTTPError as exc:
        raise SystemExit(f"Failed to fetch metrics: {exc}")
    csv_data = export_csv(data)
    if args.push_url:
        try:
            _push_metrics(csv_data, args.push_url, args.token)
        except HTTPError as exc:
            raise SystemExit(f"Failed to push metrics: {exc}")
    if args.file == "-":
        print(csv_data, end="")
    else:
        Path(args.file).write_text(csv_data)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
