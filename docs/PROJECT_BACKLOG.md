
# Project Backlog (MoSCoW)

| ID   | Pri | Title                               | Status | Notes |
|------|-----|-------------------------------------|--------|-------|
| B‑1 | **v0.5** Inventory Detection | Fine‑tune YOLOv8 on 3 k brick images | CV lead | ⬜ |
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
|------|-----|---------------------------------------|--------|-------|
| S-10 | **M** | Introduce `ILPSolver` interface & refactor | **Done** | Branch `feature/solver-refactor` |
| S-11 | **M** | Implement OR-Tools MIP constraints   | **Done** | Connectivity filter added; solver computes stable subset |
| S-12 | **S** | Solver auto-loader + unit tests      | **Done** | Part of solver refactor |
| S-13 | **XS**| Update docs for solver swap          | **Done** | README & ARCHITECTURE |

### Legend
* **Pri** – MoSCoW priority (**M**ust, **S**hould, **C**ould, **W**on’t-Have-Now).
* **Status** – Open / WIP / Blocked / Done.

_Last updated 2025-05-27_
