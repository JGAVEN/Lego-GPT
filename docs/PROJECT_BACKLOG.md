
# Project Backlog (MoSCoW)

| ID   | Pri | Title                               | Status | Notes |
|------|-----|-------------------------------------|--------|-------|
| B‑1 | **v0.5** Inventory Detection | Fine‑tune YOLOv8 on 3 k brick images | CV lead | WIP: training script added |
| B‑2 | v0.5 | Build `detector/` micro‑service, Dockerfile, RQ worker | CV lead | **Done** |
| B‑3 | v0.5 | Add `/detect_inventory` endpoint in Gateway + tests | Backend | **Done** |
| B‑4 | v0.5 | Front‑end camera / upload workflow + inventory table | FE | **Done** |
| B‑5 | v0.5 | Pass `inventory_filter` into `inference.generate()` | Backend | **Done** |
| B‑6 | v0.5 | E2E Cypress test: photo fixture → constrained build | QA | _Removed_ |
| B-01 | **M** | Dockerise backend & worker           | **Done** | GPU-aware image, `docker compose dev` |
| B-02 | **M** | React PWA scaffold                   | **Done** | Vite + Tailwind, SW cache |
| B-03 | **M** | `/generate` endpoint                 | **Done** | Async job queue, return URLs |
| B-04 | **M** | React API hook + PNG preview         | **Done** | Front-end calls `/generate`, shows preview |
| B-05 | **S** | Three.js LDraw viewer                | **Done** | Loads `.ldr` via dynamic import |
| B-06 | **S** | JWT auth & rate-limit                | **Done** | Simple HMAC tokens + per-minute limit |
| B-07 | **S** | GitHub Actions CI                    | **Done** | unittest + build images |
| B-08 | **C** | AR Quick-Look export                 | **Done** | glTF pipeline |
| B-09 | **C** | Brick inventory filter               | **Done** | Fine-tune on owned parts |
| B-10 | **M** | Add MIT licence text                 | **Done** | Root and vendor licence files added |
| B-11 | **M** | Align API contract                   | **Done** | POST returns `job_id`; GET `/generate/{job_id}` yields `{png_url, ldr_url, brick_counts}` |
| B-12 | **XS** | JWT auth unit tests                  | **Done** | encode/decode helpers |
| B-13 | **XS** | Front-end lint step in CI            | **Done** | pnpm runs ESLint in workflow |
| B-14 | **S** | YOLOv8 model auto-loader            | **Done** | `DETECTOR_MODEL` env var selects weights |
| B-15 | **XS** | Console scripts for server/worker   | **Done** | `lego-gpt-server`, `lego-gpt-worker`, `lego-detect-worker` |
| B-16 | **XS** | Ruff lint + CI step                 | **Done** | pyproject config + workflow |
| B-17 | **XS** | Configurable CORS headers            | **Done** | `--cors-origins` CLI + tests |
| B-18 | **S** | Customisable static URL prefix       | **Done** | `STATIC_URL_PREFIX` env var |
| B-19 | **C** | Upload assets to S3/R2               | **Done** | Optional CDN support |
| B-20 | **XS** | `lego-gpt-cli` command-line client    | **Done** | Python script to call the API |
| B-21 | **XS** | CLI `--version` flag and tests        | **Done** | Unit tests cover the new flag |
| B-22 | **XS** | `.env` configuration support          | **Done** | Load variables via python-dotenv |
| B-23 | **XS** | Static asset cleanup script           | **Done** | `lego-gpt-cleanup` removes old assets |
| B-24 | **XS** | `lego-gpt-cleanup` dry-run option     | **Done** | Preview deletions with `--dry-run` |
|------|-----|---------------------------------------|--------|-------|
| S-10 | **M** | Introduce `ILPSolver` interface & refactor | **Done** | Branch `feature/solver-refactor` |
| S-11 | **M** | Implement OR-Tools MIP constraints   | **Done** | Connectivity filter added; solver computes stable subset |
| S-12 | **S** | Solver auto-loader + unit tests      | **Done** | Part of solver refactor |
| S-13 | **XS**| Update docs for solver swap          | **Done** | README & ARCHITECTURE |
| B-25 | **XS** | JWT token CLI (`lego-gpt-token`) | **Done** | Generates auth tokens from the command line |
| B-26 | **XS** | CLI `--inventory` option | **Done** | Supply brick counts via JSON file |
| B-27 | **XS** | CLI loads `.env` | **Done** | `API_URL` and `JWT` automatically read |
| S-14 | **XS** | Configurable OR-Tools backend (`ORTOOLS_ENGINE`) | **Done** | Worker `--solver-engine` flag |
| B-28 | **XS** | `lego-gpt-export` CLI for LDraw → glTF | **Done** | Converts models for AR |
| B-29 | **XS** | Configurable API base URL in front-end (`VITE_API_URL`) | **Done** | `.env.example` added |
| B-30 | **XS** | CLI `generate` downloads assets via `--out-dir` | **Done** | Saves PNG/ldr/gltf locally |
| S-15 | **XS** | Log to file via `--log-file` / `LOG_FILE` | **Done** | Server & workers support file logging |
| B-31 | **XS** | `--inventory` option for server and worker | **Done** | Override `BRICK_INVENTORY` via CLI |
| B-32 | **S**  | Progress polling on `/generate/{job_id}` | **Done** | 202 responses include `progress` JSON |
| B-33 | **S**  | Redis caching for `/detect_inventory` | **Done** | Speeds up repeated detections |



### Legend
* **Pri** – MoSCoW priority (**M**ust, **S**hould, **C**ould, **W**on’t-Have-Now).
* **Status** – Open / WIP / Blocked / Done.

_Last updated 2025-06-16_
