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
from urllib import request
from urllib.error import HTTPError


def _extract_error(exc: HTTPError) -> str:
    """Return a user-friendly message from an ``HTTPError``."""
    try:
        data = exc.read().decode()
        detail = json.loads(data).get("detail", data)
        return str(detail)
    except Exception:  # pragma: no cover - malformed error
        return exc.reason

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
    try:
        with request.urlopen(req) as resp:
            return json.load(resp)
    except HTTPError as exc:  # pragma: no cover - simple CLI
        msg = _extract_error(exc)
        raise RuntimeError(f"POST {url} failed ({exc.code}): {msg}") from None


def _poll(url: str, token: str, progress: bool = False) -> dict:
    while True:
        req = request.Request(url, headers={"Authorization": f"Bearer {token}"})
        try:
            with request.urlopen(req) as resp:
                if resp.status == 200:
                    if progress:
                        print("", file=sys.stderr)
                    return json.load(resp)
        except HTTPError as exc:  # pragma: no cover - simple CLI
            if exc.code == 202:
                if progress:
                    print(".", end="", file=sys.stderr, flush=True)
                time.sleep(1)
                continue
            msg = _extract_error(exc)
            raise RuntimeError(f"GET {url} failed ({exc.code}): {msg}") from None
        time.sleep(1)


def _stream_progress(url: str) -> None:
    """Print progress dots from a Server-Sent Events endpoint."""
    try:
        with request.urlopen(url) as resp:
            for line in resp:
                if line.startswith(b"data:"):
                    print(".", end="", file=sys.stderr, flush=True)
    except Exception:  # pragma: no cover - best effort
        pass
    print("", file=sys.stderr)


def cmd_generate(args: argparse.Namespace) -> None:
    prompts: list[str] = []
    if args.file:
        with open(args.file) as f:
            prompts.extend([p.strip() for p in f if p.strip()])
    if args.prompt:
        prompts.append(args.prompt)
    if not prompts:
        raise SystemExit("Prompt or --file required")

    inv: dict | None = None
    if args.inventory:
        with open(args.inventory) as f:
            inv = json.load(f)
            if not isinstance(inv, dict):
                raise ValueError("Inventory JSON must be an object")

    for idx, prompt in enumerate(prompts, 1):
        payload = {"prompt": prompt, "seed": args.seed}
        if inv is not None:
            payload["inventory_filter"] = inv
        try:
            print(f"[{idx}/{len(prompts)}] Generating '{prompt}'", file=sys.stderr)
            res = _post(f"{args.url}/generate", args.token, payload)
            job_id = res["job_id"]
            _stream_progress(f"{args.url}/progress/{job_id}")
            result = _poll(f"{args.url}/generate/{job_id}", args.token)
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
            continue
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
    try:
        res = _post(f"{args.url}/detect_inventory", args.token, {"image": img_b64})
        job_id = res["job_id"]
        _stream_progress(f"{args.url}/progress/{job_id}")
        result = _poll(
            f"{args.url}/detect_inventory/{job_id}", args.token
        )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return
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
    g.add_argument("prompt", nargs="?", help="Text prompt")
    g.add_argument("--file", help="Path to text file with prompts")
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
