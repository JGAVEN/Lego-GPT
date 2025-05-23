"""RQ worker dedicated to brick inventory detection."""
from redis import Redis
from rq import Worker, Connection

from backend.worker import QUEUE_NAME, detect_job


def run_detector(redis_url: str = "redis://localhost:6379/0") -> None:
    """Run an RQ worker that processes detection jobs."""
    conn = Redis.from_url(redis_url)
    with Connection(conn):
        worker = Worker([QUEUE_NAME])
        worker.work()


if __name__ == "__main__":  # pragma: no cover
    run_detector()
