
# Architecture

```
┌──────────────┐   HTTPS POST /generate   ┌────────────────────────────────────────┐
│  PWA Client  │◄────────────────────────►│   HTTP Gateway (API)                │
│  React +     │                          │   • JWT auth + rate limit                 │
│  Three.js    │ PNG preview + .ldr file  │   • Task queue (Redis / RQ)           │
└────▲─────────┘                          │   • Solver shim import (side-effect)  │
     │                                    └──────────▲────────────────────────────┘
     │                                                   │
     │  .ldr parsed & viewed                             │
     ▼                                                   │
Three.js LDrawViewer                        LegoGPT model (Llama-3 1B)
                                                  ▲
                                                  │ bricks
                                                  ▼
                                   ┌─────────────────────────────────┐
                                   │  ILP Solver Layer               │
                                   │  • OR-Tools 9.10 + HiGHS (default)│
                                   │  • Gurobi (fallback if licenced)│
                                   └─────────────────────────────────┘
```

### Solver shim  
`backend/solver/shim.py` monkey-patches  
`legogpt.stability_analysis.stability_score` **before** the model loads.  
The auto-loader picks the first backend available:

1. **OR-Tools / HiGHS** – MIT, no licence.  
2. **Gurobi** – used only if a licence file is present.
3. If neither is found, shim returns a perfect score and tags previews
   **UNVERIFIED** (dev mode).

The OR-Tools backend checks each brick for support and filters out
clusters not connected to the ground.

---

## Layer Responsibilities

| Layer      | Responsibility                                                                                 | Tech / Notes |
|------------|-------------------------------------------------------------------------------------------------|--------------|
| **Front-end** | Prompt form, spinner, preview image, 3-D viewer, offline PWA shell                            | React 18, Vite, Three.js (`LDrawLoader` from CDN) |
| **API**       | Auth, rate-limit, enqueue job, expose static file links                                       | Python http.server stub |
| **Worker**    | `backend/worker.py` runs `rq` jobs, lazy-loads LegoGPT, routes bricks → solver, saves PNG + LDR | Python 3.12, CUDA 12.2, HF `transformers` |
| **Solver**    | Verify physical stability via MIP (connectivity, gravity, overhang)                           | OR-Tools / HiGHS (default), Gurobi optional |
| **Storage**   | Serve artifacts, 7-day TTL, promote to S3 / Cloudflare R2 in prod                             | Local `/static` → CDN later |

---

## Data Flow

1. **POST /generate** — client sends `{prompt, seed}`.
2. API validates, enqueues job on the Redis/RQ queue → ✅ returns `job_id`.
3. Worker loads LegoGPT, **calls solver shim** ➜ bricks verified.
4. Worker writes `preview.png` + `model.ldr` to `/static/{uuid}/`.
5. When finished, a GET on `/generate/{job_id}` returns `{png_url, ldr_url, brick_counts}`.
6. Client shows PNG immediately; Three.js lazily loads LDR → interactive viewer.
   The `LDrawLoader` module is fetched from a CDN at runtime.

---

## Scaling Notes

* **Baseline**: single GPU container (A10G 24 GB) → ≈2 s/token, 3 req/s.  
* **Horizontal**: add Redis-RQ queue + N workers when concurrency > 5.  
* **Static assets**: move `/static` to R2 or S3 + CloudFront for global latency.  
* **Model optimisations**: quantise to INT4 for CPU-only fallback; distil for mobile.  
* **Solver speed**: HiGHS handles typical models < 5 ms; Gurobi ≈ 2 ms on licence-enabled nodes.

---

_Last updated 2025-05-17_
