"""Console script to generate JWT tokens for the API."""
from __future__ import annotations

import argparse
import os
from datetime import datetime, timedelta

from backend.auth import encode


def generate_token(secret: str, sub: str, lifetime: int) -> str:
    """Return a JWT token signed with ``secret``."""
    exp_ts = int((datetime.utcnow() + timedelta(seconds=lifetime)).timestamp())
    return encode({"sub": sub}, secret, exp=exp_ts)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Generate JWT token for Lego GPT API")
    parser.add_argument(
        "--secret",
        "-s",
        default=os.getenv("JWT_SECRET", "secret"),
        help="HMAC secret (default: env JWT_SECRET or 'secret')",
    )
    parser.add_argument("--sub", default="dev", help="Subject claim (default: dev)")
    parser.add_argument(
        "--exp",
        type=int,
        default=3600,
        help="Token lifetime in seconds (default: 3600)",
    )
    args = parser.parse_args(argv)
    token = generate_token(args.secret, args.sub, args.exp)
    print(token)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
