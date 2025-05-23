
# Project Backlog (MoSCoW)

| ID   | Pri | Title                               | Status | Notes |
|------|-----|-------------------------------------|--------|-------|
| B-01 | **M** | Dockerise backend & worker           | **Done** | GPU-aware image, `docker compose dev` |
| B-02 | **M** | React PWA scaffold                   | **Done** | Vite + Tailwind, SW cache |
| B-03 | **M** | `/generate` endpoint                 | **Done** | Async job queue, return URLs |
| B-04 | **M** | React API hook + PNG preview         | **Done** | Front-end calls `/generate`, shows preview |
| B-05 | **S** | Three.js LDraw viewer                | **Blocked** | Depends on B-04 |
| B-06 | **S** | JWT auth & rate-limit                | **Open** | Prevent abuse |
| B-07 | **S** | GitHub Actions CI                    | **Done** | unittest + build images |
| B-08 | **C** | AR Quick-Look export                 | **Open** | glTF pipeline |
| B-09 | **C** | Brick inventory filter               | **Open** | Fine-tune on owned parts |
| B-10 | **M** | Add MIT licence text                 | **Done** | Root and vendor licence files added |
| B-11 | **M** | Align API contract                   | **Done** | POST returns `job_id`; GET `/generate/{job_id}` yields `{png_url, ldr_url, brick_counts}` |
|------|-----|---------------------------------------|--------|-------|
| S-10 | **M** | Introduce `ILPSolver` interface & refactor | **Done** | Branch `feature/solver-refactor` |
| S-11 | **M** | Implement OR-Tools MIP constraints   | **WIP** | Connectivity, gravity, overhang; solver shim returns dummy score |
| S-12 | **S** | Solver auto-loader + unit tests      | **Done** | Part of solver refactor |
| S-13 | **XS**| Update docs for solver swap          | **Done** | README & ARCHITECTURE |

### Legend
* **Pri** – MoSCoW priority (**M**ust, **S**hould, **C**ould, **W**on’t-Have-Now).
* **Status** – Open / WIP / Blocked / Done.

_Last updated 2025-05-23_
