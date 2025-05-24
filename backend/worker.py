"""RQ worker for asynchronous generation jobs."""
from redis import Redis
from rq import Worker, Connection
import os
from backend.api import generate_lego_model
from backend.detector import detect_inventory
from backend import __version__

QUEUE_NAME = os.getenv("QUEUE_NAME", "legogpt")


def generate_job(
    prompt: str,
    seed: int | None = 42,
    inventory_filter: dict[str, int] | None = None,
) -> dict:
    """Background job that runs the model and returns file URLs."""
    return generate_lego_model(prompt, seed, inventory_filter)


def detect_job(image_b64: str) -> dict:
    """Background job that detects brick counts from a photo."""
    counts = detect_inventory(image_b64)
    return {"brick_counts": counts}


def run_worker(
    redis_url: str = "redis://localhost:6379/0",
    queue_name: str = QUEUE_NAME,
) -> None:
    """Start an RQ worker that processes generation jobs."""
    conn = Redis.from_url(redis_url)
    with Connection(conn):
        worker = Worker([queue_name])
        worker.work()


def main(argv: list[str] | None = None) -> None:
    """CLI entry point for ``lego-gpt-worker``."""
    import argparse

    parser = argparse.ArgumentParser(description="Run Lego GPT RQ worker")
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

    run_worker(args.redis_url, args.queue)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
