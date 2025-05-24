#!/usr/bin/env python3
"""Command-line client for the Lego GPT API."""

from __future__ import annotations

import argparse
import base64
import json
import os
import time
from urllib import error, request


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
        except error.HTTPError as exc:  # pragma: no cover - simple CLI
            if exc.code == 202:
                time.sleep(1)
                continue
            raise
        time.sleep(1)


def cmd_generate(args: argparse.Namespace) -> None:
    res = _post(f"{args.url}/generate", args.token, {"prompt": args.prompt, "seed": args.seed})
    job_id = res["job_id"]
    result = _poll(f"{args.url}/generate/{job_id}", args.token)
    print(json.dumps(result, indent=2))


def cmd_detect(args: argparse.Namespace) -> None:
    with open(args.image, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    res = _post(f"{args.url}/detect_inventory", args.token, {"image": img_b64})
    job_id = res["job_id"]
    result = _poll(f"{args.url}/detect_inventory/{job_id}", args.token)
    print(json.dumps(result, indent=2))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Lego GPT API client")
    parser.add_argument("--url", default=os.getenv("API_URL", "http://localhost:8000"), help="API base URL")
    parser.add_argument("--token", default=os.getenv("JWT"), help="JWT auth token or JWT env var")
    sub = parser.add_subparsers(dest="cmd")
    g = sub.add_parser("generate", help="Generate a model from text")
    g.add_argument("prompt", help="Text prompt")
    g.add_argument("--seed", type=int, default=42, help="Random seed")
    g.set_defaults(func=cmd_generate)
    d = sub.add_parser("detect", help="Detect brick inventory from an image")
    d.add_argument("image", help="Path to image file")
    d.set_defaults(func=cmd_detect)
    args = parser.parse_args(argv)
    if not args.cmd:
        parser.print_help()
        return
    if not args.token:
        parser.error("Auth token required (use --token or set JWT)")
    args.func(args)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
