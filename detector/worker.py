"""RQ worker dedicated to brick inventory detection."""
from redis import Redis
from rq import Worker, Connection
import os
from backend import __version__
from backend.worker import QUEUE_NAME


def run_detector(
    redis_url: str = "redis://localhost:6379/0",
    queue_name: str = QUEUE_NAME,
) -> None:
    """Run an RQ worker that processes detection jobs."""
    conn = Redis.from_url(redis_url)
    with Connection(conn):
        worker = Worker([queue_name])
        worker.work()


def main(argv: list[str] | None = None) -> None:
    """CLI entry point for ``lego-detect-worker``."""
    import argparse

    parser = argparse.ArgumentParser(description="Run Lego GPT detector worker")
    parser.add_argument(
        "--redis-url",
        default=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        help="Redis connection URL (default: env REDIS_URL or redis://localhost:6379/0)",
    )
    parser.add_argument(
        "--queue",
        default=os.getenv("QUEUE_NAME", QUEUE_NAME),
        help="RQ queue name (default: env QUEUE_NAME or 'legogpt')",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print backend version and exit",
    )
    args = parser.parse_args(argv)

    if args.version:
        print(__version__)
        return

    run_detector(args.redis_url, args.queue)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
