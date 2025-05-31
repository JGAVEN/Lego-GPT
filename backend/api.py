"""Minimal API functions for offline use."""
from __future__ import annotations

import json
import os
import time
import argparse

from redis import Redis
from rq import Queue, Retry
try:
    from rq.job import Job
except Exception:  # pragma: no cover - fallback for older/stub versions
    from rq import Job
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Response,
    status,
)
from pydantic import BaseModel
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import run_in_threadpool
import uvicorn

from backend import (
    __version__,
    REDIS_URL,
    HISTORY_ROOT,
)
from backend.auth import decode as decode_jwt


def health() -> dict:
    """Return service liveness and version information."""
    redis_ok = True
    try:
        conn = Redis.from_url(REDIS_URL)
        if hasattr(conn, "ping"):
            conn.ping()
    except Exception:
        redis_ok = False
    return {"ok": redis_ok, "version": __version__, "redis": redis_ok}




JWT_SECRET = os.getenv("JWT_SECRET", "secret")
RATE_LIMIT = int(os.getenv("RATE_LIMIT", "10"))

redis_conn = Redis.from_url(REDIS_URL)
QUEUE_NAME = os.getenv("QUEUE_NAME", "legogpt")
queue = Queue(QUEUE_NAME, connection=redis_conn)
DEFAULT_RETRY = Retry(max=3, interval=[10, 30, 60])

_TOKEN_USAGE: dict[str, tuple[int, int]] = {}

METRICS = {
    "generate_requests": 0,
    "detect_requests": 0,
    "example_submissions": 0,
    "example_reports": 0,
    "token_usage": 0,
    "rate_limit_hits": 0,
}

METRICS_HISTORY: dict[str, dict[int, int]] = {
    "token_usage": {},
    "rate_limit_hits": {},
}


def _prometheus_metrics() -> str:
    lines = []
    for key, val in METRICS.items():
        lines.append(f"# TYPE lego_gpt_{key} counter")
        lines.append(f"lego_gpt_{key} {val}")
    return "\n".join(lines) + "\n"


def _record_history(key: str) -> None:
    now_min = int(time.time() // 60)
    hist = METRICS_HISTORY.setdefault(key, {})
    hist[now_min] = hist.get(now_min, 0) + 1
    for ts in list(hist):
        if now_min - ts > 59:
            del hist[ts]


bearer = HTTPBearer(auto_error=False)


def _rate_limit(token: str) -> None:
    now = int(time.time())
    window = now // 60
    count, win = _TOKEN_USAGE.get(token, (0, window))
    if win != window:
        count = 0
        win = window
    if count >= RATE_LIMIT:
        METRICS["rate_limit_hits"] += 1
        _record_history("rate_limit_hits")
        raise HTTPException(status_code=429, detail="rate_limit")
    _TOKEN_USAGE[token] = (count + 1, win)


async def _auth(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> tuple[dict, str]:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = credentials.credentials
    try:
        payload = decode_jwt(token, JWT_SECRET)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    _rate_limit(token)
    METRICS["token_usage"] += 1
    _record_history("token_usage")
    return payload, token


def _admin(payload_and_token: tuple[dict, str] = Depends(_auth)) -> dict:
    payload, _ = payload_and_token
    if payload.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return payload


app = FastAPI(title="Lego-GPT API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_route() -> dict:
    return await run_in_threadpool(health)


class GenerateRequest(BaseModel):
    prompt: str = ""
    seed: int | None = 42
    inventory_filter: dict[str, int] | None = None


class ImageRequest(BaseModel):
    image: str


@app.post("/generate")
async def generate_route(
    req: GenerateRequest,
    auth: tuple[dict, str] = Depends(_auth),
) -> dict:
    payload, _token = auth
    from backend.worker import generate_job  # imported here to avoid circular dependency

    job = await run_in_threadpool(
        queue.enqueue,
        generate_job,
        req.prompt,
        req.seed or 42,
        req.inventory_filter,
        retry=DEFAULT_RETRY,
    )
    job.meta["user"] = payload.get("sub", "user")
    job.meta["prompt"] = req.prompt
    job.meta["seed"] = req.seed or 42
    job.save_meta()
    METRICS["generate_requests"] += 1
    return {"job_id": job.id}


@app.get("/generate/{job_id}")
async def generate_result_route(
    job_id: str,
    auth: tuple[dict, str] = Depends(_auth),
) -> Response:
    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception:
        raise HTTPException(status_code=404)
    if job.is_finished:
        return job.result
    if job.is_failed:
        raise HTTPException(status_code=500, detail="Job failed")
    return Response(status_code=202)


@app.post("/detect_inventory")
async def detect_inventory_route(
    req: ImageRequest,
    auth: tuple[dict, str] = Depends(_auth),
) -> dict:
    payload, _token = auth
    from backend.worker import detect_job  # imported here to avoid circular dependency

    job = await run_in_threadpool(
        queue.enqueue,
        detect_job,
        req.image,
        retry=DEFAULT_RETRY,
    )
    job.meta["user"] = payload.get("sub", "user")
    job.save_meta()
    METRICS["detect_requests"] += 1
    return {"job_id": job.id}


@app.get("/detect_inventory/{job_id}")
async def detect_inventory_result_route(
    job_id: str,
    auth: tuple[dict, str] = Depends(_auth),
) -> Response:
    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception:
        raise HTTPException(status_code=404)
    if job.is_finished:
        result = job.result
        user = job.meta.get("user")
        if user:
            HISTORY_ROOT.mkdir(parents=True, exist_ok=True)
            file_path = HISTORY_ROOT / f"{user}.jsonl"
            record = {
                "prompt": job.meta.get("prompt", ""),
                "seed": job.meta.get("seed", 42),
                "result": result,
                "ts": int(time.time()),
            }
            with open(file_path, "a") as fh:
                fh.write(json.dumps(record) + "\n")
        return result
    if job.is_failed:
        raise HTTPException(status_code=500, detail="Job failed")
    return Response(status_code=202)


@app.get("/metrics")
async def metrics_route(admin: dict = Depends(_admin)) -> dict:
    payload = dict(METRICS)
    payload["history"] = {k: sorted(v.items()) for k, v in METRICS_HISTORY.items()}
    return payload


@app.get("/metrics_prom")
async def metrics_prom_route(admin: dict = Depends(_admin)) -> Response:
    data = await run_in_threadpool(_prometheus_metrics)
    return Response(content=data, media_type="text/plain; version=0.0.4")


@app.get("/history")
async def history_route(auth: tuple[dict, str] = Depends(_auth)) -> dict:
    payload, _token = auth
    user = payload.get("sub", "user")
    file_path = HISTORY_ROOT / f"{user}.jsonl"
    if file_path.is_file():
        entries = [json.loads(line) for line in file_path.read_text().splitlines()]
    else:
        entries = []
    return {"history": entries}


def main() -> None:
    """Run the FastAPI server via uvicorn."""
    parser = argparse.ArgumentParser(description="Run Lego GPT FastAPI server")
    parser.add_argument("--host", default=os.getenv("HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8000")))
    parser.add_argument(
        "--reload", action="store_true", help="Enable auto-reload for development"
    )
    args = parser.parse_args()
    uvicorn.run("backend.api:app", host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()

