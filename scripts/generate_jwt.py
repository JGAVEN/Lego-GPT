#!/usr/bin/env python3
"""Helper script to generate JWT tokens for the API."""

import argparse
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.auth import encode


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate JWT token for Lego GPT API")
    parser.add_argument(
        "--secret",
        "-s",
        default=os.getenv("JWT_SECRET", "secret"),
        help="HMAC secret (defaults to JWT_SECRET env var)",
    )
    parser.add_argument("--sub", default="dev", help="Subject claim (default: dev)")
    parser.add_argument(
        "--exp",
        type=int,
        default=3600,
        help="Token lifetime in seconds (default: 3600)",
    )
    args = parser.parse_args()
    exp_ts = int((datetime.utcnow() + timedelta(seconds=args.exp)).timestamp())
    token = encode({"sub": args.sub}, args.secret, exp=exp_ts)
    print(token)


if __name__ == "__main__":
    main()
