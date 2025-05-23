
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
                                   │  • OR-Tools 9.10 + HiGHS│
                                   └─────────────────────────────────┘
```

### Solver shim  
`backend/solver/shim.py` monkey-patches  
`legogpt.stability_analysis.stability_score` **before** the model loads.  
The auto-loader picks the first backend available:

1. **OR-Tools / HiGHS** – MIT, no licence required.
2. If not available, the shim returns a perfect score and tags previews
   **UNVERIFIED** (dev mode).

The OR-Tools backend checks each brick for support and filters out
clusters not connected to the ground.

---

## Layer Responsibilities

| Layer      | Responsibility                                                                                 | Tech / Notes |
|------------|-------------------------------------------------------------------------------------------------|--------------|
| **Front-end** | Prompt form, spinner, preview image, 3-D viewer, offline PWA shell                            | React 18, Vite, Three.js (`LDrawLoader` from CDN) |
| **API**       | Auth, rate-limit, enqueue job, expose static file links                                       | Python http.server stub |
| **Worker**    | `lego-gpt-worker` runs `rq` jobs, lazy-loads LegoGPT, routes bricks → solver, saves PNG + LDR | Python 3.12, CUDA 12.2, HF `transformers` |
| **Solver**    | Verify physical stability via MIP (connectivity, gravity, overhang)                           | OR-Tools / HiGHS |
| **Storage**   | Serve artifacts, 7-day TTL, promote to S3 / Cloudflare R2 in prod                             | Local `/static` → CDN later |

---

## Data Flow

1. **POST /generate** — client sends `{prompt, seed}`.
2. API validates, enqueues job on the Redis/RQ queue → ✅ returns `job_id`.
3. Worker loads LegoGPT, **calls solver shim** ➜ bricks verified.
4. Inventory filter trims the brick list using `BRICK_INVENTORY`.
5. Worker writes `preview.png`, `model.ldr`, and `model.gltf` to
   `backend/static/{uuid}/` by default (`STATIC_ROOT` can override).
6. When finished, a GET on `/generate/{job_id}` returns `{png_url, ldr_url, gltf_url, brick_counts}`.
7. Client shows PNG immediately; Three.js lazily loads LDR → interactive viewer.
   The `LDrawLoader` module is fetched from a CDN at runtime.

---

## Scaling Notes

* **Baseline**: single GPU container (A10G 24 GB) → ≈2 s/token, 3 req/s.  
* **Horizontal**: add Redis-RQ queue + N workers when concurrency > 5.  
* **Static assets**: move `/static` to R2 or S3 + CloudFront for global latency.  
* **Model optimisations**: quantise to INT4 for CPU-only fallback; distil for mobile.  
* **Solver speed**: HiGHS handles typical models < 5 ms.

---

_Last updated 2025-05-29_

---

## Brick‑Detector Micro‑service (new in v0.5.0)

Adds a YOLOv8‑based computer‑vision worker that converts user‑supplied photos into an inventory map `{ part_id: count }`. The gateway exposes `/detect_inventory`, and the PWA includes an `InventoryScanner` component (hook `useDetectInventory`) so users can upload a photo, review the detected parts list and generate a model constrained to their bricks.

The API validates that the `image` field contains a valid base64 string and
returns HTTP 400 for malformed data.

The worker lives in the top-level `detector/` directory and can run as a
standalone micro‑service via `detector/Dockerfile.dev`. Start it locally with the
`lego-detect-worker` console script. The dev Dockerfiles install all backend
dependencies so the container starts without extra setup.

Set the `DETECTOR_MODEL` environment variable to the path of the YOLOv8
weights file.  If the variable is unset or the `ultralytics` package is
missing the worker falls back to a small stub that returns a fixed
inventory map for testing.

```
[User Phone]
     │  photos
     ▼
Gateway  ──►  Redis Job  ──►  Brick‑Detector Worker (YOLOv8)  ──►  inventory JSON
```
