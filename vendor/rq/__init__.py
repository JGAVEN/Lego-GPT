"""Minimal rq stub for offline tests."""
from __future__ import annotations

import uuid
from typing import Any, Callable, Iterable

_job_registry: dict[str, 'Job'] = {}

class Job:
    """Simple representation of a queued job."""
    def __init__(self, func: Callable[..., Any], args: tuple[Any, ...], kwargs: dict[str, Any]):
        self.id = str(uuid.uuid4())
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result: Any | None = None
        self._status = 'queued'
        _job_registry[self.id] = self

    @property
    def is_finished(self) -> bool:
        return self._status == 'finished'

    @property
    def is_failed(self) -> bool:
        return self._status == 'failed'

    @classmethod
    def fetch(cls, job_id: str, connection: Any | None = None) -> 'Job':
        return _job_registry[job_id]

class Queue:
    def __init__(self, name: str = 'default', connection: Any | None = None):
        self.name = name
        self.connection = connection
        self.jobs: list[Job] = []

    def enqueue(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Job:
        job = Job(func, args, kwargs)
        self.jobs.append(job)
        return job


class Retry:
    """Placeholder for rq Retry settings."""
    def __init__(self, max: int = 0, interval: list[int] | None = None):
        self.max = max
        self.interval = interval or []

class SimpleWorker:
    def __init__(self, queues: Iterable[Queue], connection: Any | None = None):
        self.queues = list(queues)
        self.connection = connection

    def work(self, burst: bool = True) -> None:
        for queue in list(self.queues):
            for job in list(queue.jobs):
                try:
                    job.result = job.func(*job.args, **job.kwargs)
                    job._status = 'finished'
                except Exception:
                    job._status = 'failed'
                queue.jobs.remove(job)

class Connection:
    def __init__(self, connection: Any):
        self.connection = connection
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        return False

class Worker(SimpleWorker):
    pass
