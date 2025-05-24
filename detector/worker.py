"""RQ worker dedicated to brick inventory detection."""
from redis import Redis
from rq import Worker, Connection
import os

from backend.worker import QUEUE_NAME, detect_job


def run_detector(redis_url: str = "redis://localhost:6379/0") -> None:
    """Run an RQ worker that processes detection jobs."""
    conn = Redis.from_url(redis_url)
    with Connection(conn):
        worker = Worker([QUEUE_NAME])
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
    args = parser.parse_args(argv)

    run_detector(args.redis_url)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
