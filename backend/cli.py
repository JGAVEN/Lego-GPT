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
from importlib import import_module


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


def _load_config_token() -> str | None:
    """Return token from ``~/.lego-gpt`` if present."""
    path = Path.home() / ".lego-gpt"
    if not path.is_file():
        return None
    try:
        data = path.read_text().strip()
        if data.startswith("{"):
            return json.loads(data).get("token")
        return data
    except Exception:  # pragma: no cover - ignore errors
        return None


OFFLINE_FILE = Path.home() / ".lego-gpt-offline.json"


def _queue_offline(task: dict) -> None:
    items: list[dict] = []
    if OFFLINE_FILE.is_file():
        try:
            items = json.loads(OFFLINE_FILE.read_text())
            if not isinstance(items, list):
                items = []
        except Exception:
            items = []
    items.append(task)
    OFFLINE_FILE.write_text(json.dumps(items, indent=2))


def _replay_offline(url: str, token: str) -> None:
    if not OFFLINE_FILE.is_file():
        return
    try:
        items = json.loads(OFFLINE_FILE.read_text())
        if not isinstance(items, list):
            items = []
    except Exception:
        items = []
    remaining = []
    for task in items:
        cmd = task.get("cmd")
        payload = task.get("payload", task)
        try:
            if cmd == "detect":
                print("Replaying offline detection", file=sys.stderr)
                res = _post(f"{url}/detect_inventory", token, payload)
                job_id = res["job_id"]
                result = _poll(f"{url}/detect_inventory/{job_id}", token)
            else:
                print(
                    f"Replaying offline '{payload.get('prompt','')}'",
                    file=sys.stderr,
                )
                res = _post(f"{url}/generate", token, payload)
                job_id = res["job_id"]
                result = _poll(f"{url}/generate/{job_id}", token)
            print(json.dumps(result, indent=2))
        except Exception as exc:  # pragma: no cover - network failure
            print(f"Replay failed: {exc}", file=sys.stderr)
            remaining.append(task)
    if remaining:
        OFFLINE_FILE.write_text(json.dumps(remaining, indent=2))
    else:
        OFFLINE_FILE.unlink(missing_ok=True)


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


def _load_plugins(subparsers: argparse._SubParsersAction) -> None:
    """Load CLI plugins from ``~/.lego-gpt/plugins``."""
    plugins_dir = Path.home() / ".lego-gpt" / "plugins"
    if not plugins_dir.is_dir():
        return
    sys.path.insert(0, str(plugins_dir))
    for mod_path in sorted(plugins_dir.glob("*.py")):
        try:
            mod = import_module(mod_path.stem)
            if hasattr(mod, "register"):
                mod.register(subparsers)
        except Exception as exc:  # pragma: no cover - plugin errors
            print(f"Failed to load plugin {mod_path.name}: {exc}", file=sys.stderr)


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
            print(f"Error: {exc}; queued offline", file=sys.stderr)
            _queue_offline({"cmd": "generate", "payload": payload})
            continue
        print(json.dumps(result, indent=2))
        if args.out_dir:
            out = Path(args.out_dir)
            out.mkdir(parents=True, exist_ok=True)
            for key in ["png_url", "ldr_url", "gltf_url", "instructions_url"]:
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
        print(f"Error: {exc}; queued offline", file=sys.stderr)
        _queue_offline({"cmd": "detect", "payload": {"image": img_b64}})
        return
    print(json.dumps(result, indent=2))


BASH_COMPLETION = """
_lego_gpt_cli_complete() {
    local cmds="generate detect completion"
    if [[ $COMP_CWORD == 1 ]]; then
        COMPREPLY=( $(compgen -W "$cmds" -- "${COMP_WORDS[1]}") )
    fi
}
complete -F _lego_gpt_cli_complete lego-gpt-cli
"""

ZSH_COMPLETION = """
_lego_gpt_cli_complete() {
    local -a cmds
    cmds=(generate detect completion)
    if [[ $CURRENT == 1 ]]; then
        _values 'cmds' $cmds
    fi
}
compdef _lego_gpt_cli_complete lego-gpt-cli
"""


def cmd_completion(args: argparse.Namespace) -> None:
    if args.shell == "bash":
        print(BASH_COMPLETION.strip())
    else:
        print(ZSH_COMPLETION.strip())


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
    _load_plugins(sub)
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
    c = sub.add_parser("completion", help="Output shell completion script")
    c.add_argument("shell", choices=["bash", "zsh"], help="Shell type")
    c.set_defaults(func=cmd_completion)
    args = parser.parse_args(argv)
    if args.version:
        print(__version__)
        return
    if not args.cmd:
        parser.print_help()
        return
    if not args.token:
        args.token = _load_config_token()
    if not args.token:
        parser.error("Auth token required (use --token, config file, or set JWT)")
    _replay_offline(args.url, args.token)
    args.func(args)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
