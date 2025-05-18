
# Architecture

```
┌──────────────┐   HTTPS POST /generate   ┌────────────────────────────────────────┐
│  PWA Client  │◄────────────────────────►│   FastAPI Gateway (API)                │
│  React +     │                          │   • JWT auth (future)                 │
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

---

## Layer Responsibilities

| Layer      | Responsibility                                                                                 | Tech / Notes |
|------------|-------------------------------------------------------------------------------------------------|--------------|
| **Front-end** | Prompt form, spinner, preview image, 3-D viewer, offline PWA shell                            | React 18, Vite, Three.js (`LDrawLoader`) |
| **API**       | Auth, rate-limit, enqueue job, expose static file links                                       | FastAPI, Pydantic, Redis-RQ (future Celery) |
| **Worker**    | Lazy-load LegoGPT, invoke `generate()`, route bricks → solver, save PNG + LDR                | Python 3.12, CUDA 12.2, HF `transformers` |
| **Solver**    | Verify physical stability via MIP (connectivity, gravity, overhang)                           | OR-Tools / HiGHS (default), Gurobi optional |
| **Storage**   | Serve artifacts, 7-day TTL, promote to S3 / Cloudflare R2 in prod                             | Local `/static` → CDN later |

---

## Data Flow

1. **POST /generate** — client sends `{text, seed}`.  
2. API validates, enqueues job → ✅ returns `job_id`.  
3. Worker loads LegoGPT, **calls solver shim** ➜ bricks verified.  
4. Worker writes `preview.png` + `model.ldr` to `/static/{uuid}/`.  
5. API responds `{png_url, ldr_url, brick_counts}` (or client polls on `job_id`).  
6. Client shows PNG immediately; Three.js lazily loads LDR → interactive viewer.

---

## Scaling Notes

* **Baseline**: single GPU container (A10G 24 GB) → ≈2 s/token, 3 req/s.  
* **Horizontal**: add Redis-RQ queue + N workers when concurrency > 5.  
* **Static assets**: move `/static` to R2 or S3 + CloudFront for global latency.  
* **Model optimisations**: quantise to INT4 for CPU-only fallback; distil for mobile.  
* **Solver speed**: HiGHS handles typical models < 5 ms; Gurobi ≈ 2 ms on licence-enabled nodes.

---

_Last updated 2025-05-17_
