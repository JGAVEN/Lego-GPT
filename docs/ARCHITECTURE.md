
# Architecture

All components assume English input and output. The system does not provide multilingual support.

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
| **CLI**       | Call `/generate` and `/detect_inventory` from the terminal (supports `--version`)     | `lego-gpt-cli` Python script |
| **API**       | Auth, rate-limit, CORS headers, enqueue job, expose static file links                                       | Python http.server stub |
| **Worker**    | `lego-gpt-worker` runs `rq` jobs, lazy-loads LegoGPT, routes bricks → solver, saves PNG + LDR (use `--redis-url`, `--queue`, and `--version`) | Python 3.12, CUDA 12.2, HF `transformers` |
| **Solver**    | Verify physical stability via MIP (connectivity, gravity, overhang)                           | OR-Tools / HiGHS |
| **Storage**   | Serve artifacts locally or upload to S3 / Cloudflare R2                             | `/static` or S3 bucket; `lego-gpt-cleanup` removes old files (`--dry-run` to preview) |

---

## Data Flow

1. **POST /generate** — client sends `{prompt, seed}`.
2. API validates, enqueues job on the Redis/RQ queue → ✅ returns `job_id`.
3. Worker loads LegoGPT, **calls solver shim** ➜ bricks verified.
4. Inventory filter trims the brick list using `BRICK_INVENTORY`.
5. Worker writes `preview.png`, `model.ldr`, `model.gltf`, and `instructions.pdf` to
   `backend/static/{uuid}/` by default. Pass ``--static-root <dir>``
   (or set ``STATIC_ROOT``) to override the directory. Use
   ``STATIC_URL_PREFIX`` to customise the URL prefix returned to the
   client (defaults to ``/static``).
6. If ``S3_BUCKET`` is configured, each file is gzipped and uploaded with
   ``Content-Encoding: gzip`` for efficient storage.
7. When finished, a GET on `/generate/{job_id}` returns `{png_url, ldr_url, gltf_url, instructions_url, brick_counts}`. Each completed build is logged under ``HISTORY_ROOT`` and can be retrieved via ``/history``.
8. Clients may subscribe to `/progress/{job_id}` for Server-Sent Events with
   `{"progress": 0..100}` updates.
9. Client shows PNG immediately; Three.js lazily loads LDR → interactive viewer.
   The `LDrawLoader` module is fetched from a CDN at runtime.
10. Set ``LOG_LEVEL`` or pass ``--log-level`` to server/workers to control logging verbosity.
11. Environment variables can be placed in a ``.env`` file. If
   ``python-dotenv`` is installed, the backend loads it automatically on startup.
12. Set ``ORTOOLS_ENGINE`` or pass ``--solver-engine`` to the worker to pick a
    specific OR-Tools backend (``HIGHs`` or ``CBC``).

Community members can post new prompt ideas via ``POST /submit_example``. Each
submission is stored under ``backend/submissions/`` for manual curation.
Use the ``lego-gpt-review`` CLI to list and approve these submissions.

---

## Scaling Notes

* **Baseline**: single GPU container (A10G 24 GB) → ≈2 s/token, 3 req/s.  
* **Horizontal**: add Redis-RQ queue + N workers when concurrency > 5.  
* **Static assets**: optionally upload to R2 or S3 + CloudFront for global latency.
* **Model optimisations**: quantise to INT4 for CPU-only fallback; distil for mobile.  
* **Solver speed**: HiGHS handles typical models < 5 ms.

---

_Last updated 2025-07-28_

---

## Brick‑Detector Micro‑service (new in v0.5.0)

Adds a YOLOv8‑based computer‑vision worker that converts user‑supplied photos into an inventory map `{ part_id: count }`. The FastAPI server exposes `/detect_inventory`, and the PWA includes an `InventoryScanner` component (hook `useDetectInventory`) so users can upload one or more photos, review the detected parts list and generate a model constrained to their bricks. Results from multiple photos are merged into a single inventory file.

The API validates that the `image` field contains a valid base64 string and
returns HTTP 400 for malformed data.

The worker lives in the top-level `detector/` directory and can run as a
standalone micro‑service via `detector/Dockerfile.dev`. Start it locally with the
`lego-detect-worker` console script. The dev Dockerfiles install all backend
dependencies so the container starts without extra setup.

Use the companion `lego-detect-train` script to fine‑tune the YOLOv8
model when a labelled dataset is available:

```bash
lego-detect-train data.yaml --epochs 100 --out detector/model.pt
```

Alternatively, build the training container and mount your dataset:

```bash
scripts/train_detector.sh /path/to/data.yaml --epochs 100 --out detector/model.pt
```

Refer to [DETECTOR_DATASET.md](DETECTOR_DATASET.md) for details on the expected dataset format.

Set the `DETECTOR_MODEL` environment variable (or pass ``--model`` to
``lego-detect-worker``) with the path to the YOLOv8 weights file.  If the
variable is unset or the `ultralytics` package is
missing the worker falls back to a small stub that returns a fixed
inventory map for testing.

```
[User Phone]
     │  photos
     ▼
Gateway  ──►  Redis Job  ──►  Brick‑Detector Worker (YOLOv8)  ──►  inventory JSON
```
