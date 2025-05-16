# Architecture – Lego GPT (May 2025)

```
Browser (React)
│
│ 1. POST /generate {text, seed}
▼
FastAPI Gateway ─┬─> (future) enqueue job
                 └─> LegoGPT inference (mocked)
                     │
                     ├── PNG preview
                     ├── .ldr file
                     └── brick_counts json
                     │
           saves files to backend/static/<uuid>/
                 │
2. JSON response ──> {png_url, ldr_url, brick_counts}
```

| Layer       | Implementation                     | Status |
|-------------|------------------------------------|--------|
| Front‑end   | React 18 + Vite + TS, fetch API    | scaffold only |
| 3‑D Viewer  | Three.js `LDrawLoader`             | **TODO** Ticket 2.2 |
| Gateway     | FastAPI, Pydantic                  | `/health`, `/generate` (mock model) |
| Model       | CMU LegoGPT (Llama‑3 1B)           | git‑submodule, lazy‑load mocked in tests |
| Worker      | (future) Celery/RQ GPU container   | **TODO** after real model weights |
| Static      | Starlette `StaticFiles`            | serves `/static/...` |

## Testing

* **Unit & Integration**: pytest with `TestClient`.
* **Model**: mocked via `unittest.mock` to avoid weight downloads in CI.
* `pytest.ini` sets `pythonpath = .` so `import backend` works.

## Roadmap Highlights

| Milestone | Description |
|-----------|-------------|
| Replace mock with real LegoGPT weights | Publish config.json + weights to HF; update `inference.py`. |
| Redis queue & worker | Enable multiple concurrent generations. |
| Three‑js viewer | Interactive orbit/pinch of generated builds. |
| Auth & rate‑limit | JWT + IP throttling to prevent abuse. |
