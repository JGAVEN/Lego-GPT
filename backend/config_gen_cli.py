from __future__ import annotations

import argparse
from pathlib import Path

SAMPLE_CONFIG = """# Sample Lego GPT configuration
JWT_SECRET: change-me
REDIS_URL: redis://localhost:6379/0
RATE_LIMIT: 5
QUEUE_NAME: default
STATIC_ROOT: backend/static
STATIC_URL_PREFIX: /static
LOG_LEVEL: INFO
"""

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Generate sample YAML config")
    parser.add_argument(
        "path",
        nargs="?",
        help="Output path (defaults to stdout)",
    )
    args = parser.parse_args(argv)
    if args.path:
        Path(args.path).write_text(SAMPLE_CONFIG)
    else:
        print(SAMPLE_CONFIG)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
