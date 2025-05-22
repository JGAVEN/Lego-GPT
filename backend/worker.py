"""RQ worker for asynchronous generation jobs."""
from redis import Redis
from rq import Worker, Queue, Connection
from backend.api import generate_lego_model

QUEUE_NAME = "legogpt"


def generate_job(prompt: str, seed: int | None = 42) -> dict:
    """Background job that runs the model and returns file URLs."""
    return generate_lego_model(prompt, seed)


def run_worker(redis_url: str = "redis://localhost:6379/0") -> None:
    """Entry point to start an RQ worker."""
    conn = Redis.from_url(redis_url)
    with Connection(conn):
        worker = Worker([QUEUE_NAME])
        worker.work()


if __name__ == "__main__":  # pragma: no cover
    run_worker()
