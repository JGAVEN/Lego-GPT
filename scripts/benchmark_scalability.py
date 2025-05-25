#!/usr/bin/env python3
"""Simple scalability benchmark for the Lego GPT API.

This script issues multiple concurrent `/generate` requests and measures
throughput. It reuses helper functions from ``backend.cli`` so it requires no
extra dependencies.
"""

from __future__ import annotations

import argparse
import concurrent.futures as futures
import statistics
import time
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend import cli


def _generate(prompt: str, url: str, token: str, seed: int) -> None:
    """Send a generate request and wait for completion."""
    res = cli._post(f"{url}/generate", token, {"prompt": prompt, "seed": seed})
    cli._poll(f"{url}/generate/{res['job_id']}", token)


def benchmark(url: str, token: str, prompt: str, seed: int, requests: int, concurrency: int) -> None:
    """Run the benchmark and print results."""
    start = time.perf_counter()
    durations = []
    with futures.ThreadPoolExecutor(max_workers=concurrency) as ex:
        future_to_start: dict[futures.Future[None], float] = {}
        for idx in range(requests):
            p = f"{prompt} {idx}"
            future = ex.submit(_generate, p, url, token, seed)
            future_to_start[future] = time.perf_counter()
        for future in futures.as_completed(future_to_start):
            fut_start = future_to_start[future]
            future.result()
            durations.append(time.perf_counter() - fut_start)
    total = time.perf_counter() - start
    print(f"Completed {requests} requests in {total:.2f}s")
    if durations:
        print(f"Avg latency: {statistics.mean(durations):.2f}s")
        print(f"Throughput: {requests / total:.2f} req/s")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Benchmark Lego GPT throughput")
    parser.add_argument("--url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--token", required=True, help="JWT auth token")
    parser.add_argument("--prompt", default="test model", help="Prompt text")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--requests", type=int, default=10, help="Number of requests to send")
    parser.add_argument("--concurrency", type=int, default=2, help="Concurrent worker threads")
    args = parser.parse_args(argv)
    benchmark(args.url, args.token, args.prompt, args.seed, args.requests, args.concurrency)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
