# Scalability Benchmarking

> **Note**: The application launches with an English-only interface and does not support additional languages.

This guide explains how to measure API throughput and tune your deployment.

## 1. Prerequisites

* A running Redis instance and at least one `lego-gpt-worker`.
* The API server started via `lego-gpt-api`.
* A valid JWT token for authentication.

## 2. Benchmark script

Use `scripts/benchmark_scalability.py` to send concurrent generation requests:

```bash
python scripts/benchmark_scalability.py --token $JWT \
    --requests 20 --concurrency 4
```

The script prints average latency and overall throughput. Adjust `--requests`
and `--concurrency` to simulate different workloads.

## 3. Tuning guidelines

* **Workers** – Increase the number of `lego-gpt-worker` processes to handle
  more jobs concurrently. Each worker can run on a separate CPU core or GPU.
* **Queues** – Use dedicated queues for high and low priority jobs. Start
  workers with `--queue <name>` to bind them to specific queues.
* **Redis** – For heavy workloads, run Redis on a dedicated host and tune
  `maxmemory` and persistence settings for stability.
* **API server** – The gateway is lightweight, but you can run multiple
  instances behind a load balancer for high traffic scenarios.

Benchmark regularly when adjusting these parameters to find the optimal
configuration for your hardware.

## 4. Horizontal scaling

When deployment traffic increases, run multiple `lego-gpt-worker` containers.
All workers consume jobs from the same Redis queue, so you can add or remove
instances without downtime.

- **Docker Compose** – `docker compose up --scale worker=4` launches four
  worker containers.
- **Kubernetes** – configure a `HorizontalPodAutoscaler` for the worker
  deployment based on CPU or queue length metrics.

Monitor queue length and latency to adjust the scaling policy.
