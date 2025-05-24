#!/usr/bin/env python3
"""Command-line client for the Lego GPT API."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path
from urllib import error, request

# ---------------------------------------------------------------------------
#                         Optional .env loader
# ---------------------------------------------------------------------------
try:  # pragma: no cover - optional dependency
    from dotenv import load_dotenv

    load_dotenv()
except Exception:  # pragma: no cover - fallback minimal loader
    env_path = Path(".env")
    if env_path.is_file():
        for line in env_path.read_text().splitlines():
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def _post(url: str, token: str, payload: dict) -> dict:
    data = json.dumps(payload).encode()
    req = request.Request(
        url, data=data, headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    )
    with request.urlopen(req) as resp:
        return json.load(resp)


def _poll(url: str, token: str) -> dict:
    while True:
        req = request.Request(url, headers={"Authorization": f"Bearer {token}"})
        try:
            with request.urlopen(req) as resp:
                if resp.status == 200:
                    return json.load(resp)
                if resp.status == 202:
                    data = json.loads(resp.read() or b"{}")
                    progress = int(data.get("progress", 0) * 100)
                    print(f"{progress}%", file=sys.stderr)
                    time.sleep(1)
                    continue
        except error.HTTPError as exc:  # pragma: no cover - simple CLI
            if exc.code == 202:
                data = json.loads(exc.read() or b"{}")
                progress = int(data.get("progress", 0) * 100)
                print(f"{progress}%", file=sys.stderr)
                time.sleep(1)
                continue
            raise
        time.sleep(1)


def cmd_generate(args: argparse.Namespace) -> None:
    payload = {"prompt": args.prompt, "seed": args.seed}
    if args.inventory:
        with open(args.inventory) as f:
            inv = json.load(f)
            if not isinstance(inv, dict):
                raise ValueError("Inventory JSON must be an object")
        payload["inventory_filter"] = inv
    res = _post(f"{args.url}/generate", args.token, payload)
    job_id = res["job_id"]
    result = _poll(f"{args.url}/generate/{job_id}", args.token)
    print(json.dumps(result, indent=2))
    if args.out_dir:
        out = Path(args.out_dir)
        out.mkdir(parents=True, exist_ok=True)
        for key in ["png_url", "ldr_url", "gltf_url"]:
            url = result.get(key)
            if url:
                dest = out / Path(url).name
                with request.urlopen(url) as resp, open(dest, "wb") as f:
                    f.write(resp.read())


def cmd_detect(args: argparse.Namespace) -> None:
    with open(args.image, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    res = _post(f"{args.url}/detect_inventory", args.token, {"image": img_b64})
    job_id = res["job_id"]
    result = _poll(f"{args.url}/detect_inventory/{job_id}", args.token)
    print(json.dumps(result, indent=2))


from backend import __version__


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Lego GPT API client")
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print backend version and exit",
    )
    parser.add_argument("--url", default=os.getenv("API_URL", "http://localhost:8000"), help="API base URL")
    parser.add_argument("--token", default=os.getenv("JWT"), help="JWT auth token or JWT env var")
    sub = parser.add_subparsers(dest="cmd")
    g = sub.add_parser("generate", help="Generate a model from text")
    g.add_argument("prompt", help="Text prompt")
    g.add_argument("--seed", type=int, default=42, help="Random seed")
    g.add_argument(
        "--inventory",
        help="Path to brick inventory JSON file",
    )
    g.add_argument(
        "--out-dir",
        help="Directory to save generated assets",
    )
    g.set_defaults(func=cmd_generate)
    d = sub.add_parser("detect", help="Detect brick inventory from an image")
    d.add_argument("image", help="Path to image file")
    d.set_defaults(func=cmd_detect)
    args = parser.parse_args(argv)
    if args.version:
        print(__version__)
        return
    if not args.cmd:
        parser.print_help()
        return
    if not args.token:
        parser.error("Auth token required (use --token or set JWT)")
    args.func(args)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
