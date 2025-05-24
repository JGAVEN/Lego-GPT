"""RQ worker for asynchronous generation jobs."""
import os
from redis import Redis
from rq import Connection, Worker
from backend.logging_config import setup_logging
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
    try:
        from rq import get_current_job

        job = get_current_job()
    except Exception:  # pragma: no cover - executed outside RQ
        job = None
    if job is not None:
        job.meta["progress"] = 0.0
        job.save_meta()
    result = generate_lego_model(prompt, seed, inventory_filter)
    if job is not None:
        job.meta["progress"] = 1.0
        job.save_meta()
    return result


def detect_job(image_b64: str) -> dict:
    """Background job that detects brick counts from a photo."""
    counts = detect_inventory(image_b64)
    return {"brick_counts": counts}


def run_worker(
    redis_url: str = "redis://localhost:6379/0",
    queue_name: str = QUEUE_NAME,
    log_level: str | None = None,
    solver_engine: str | None = None,
    log_file: str | None = None,
    inventory_path: str | None = None,
) -> None:
    """Start an RQ worker that processes generation jobs."""
    conn = Redis.from_url(redis_url)
    setup_logging(log_level, log_file)
    if solver_engine:
        os.environ["ORTOOLS_ENGINE"] = solver_engine
    if inventory_path:
        os.environ["BRICK_INVENTORY"] = inventory_path
        import backend.inventory as inv

        inv._INVENTORY = None
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
    parser.add_argument(
        "--log-level",
        default=os.getenv("LOG_LEVEL", "INFO"),
        help="Logging level (default: env LOG_LEVEL or INFO)",
    )
    parser.add_argument(
        "--log-file",
        default=os.getenv("LOG_FILE"),
        help="File path to write logs (default: env LOG_FILE)",
    )
    parser.add_argument(
        "--solver-engine",
        default=os.getenv("ORTOOLS_ENGINE", "HIGHs"),
        help="OR-Tools solver backend (default: env ORTOOLS_ENGINE or HIGHs)",
    )
    parser.add_argument(
        "--inventory",
        default=os.getenv("BRICK_INVENTORY"),
        help="Path to brick inventory JSON (default: env BRICK_INVENTORY)",
    )
    args = parser.parse_args(argv)

    if args.version:
        print(__version__)
        return

    run_worker(
        args.redis_url,
        args.queue,
        args.log_level,
        args.solver_engine,
        args.log_file,
        args.inventory,
    )


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
