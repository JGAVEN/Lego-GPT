
# Project Backlog (MoSCoW)

The application is English-only. Multi-language user interfaces are out of scope.

| ID   | Pri | Title                               | Status | Notes |
|------|-----|-------------------------------------|--------|-------|
| B‑1 | **v0.5** Inventory Detection | Fine‑tune YOLOv8 on 3 k brick images | CV lead | **Done**: training Dockerfile and docs |
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
| B-31 | **XS** | CLI batch mode + progress output | **Done** | `--file` option and progress dots |
| B-32 | **XS** | CLI integration tests | **Done** | End-to-end CLI tests with mocked network |
| S-15 | **XS** | Log to file via `--log-file` / `LOG_FILE` | **Done** | Server & workers support file logging |
| D-21 | **M**  | Add Redis service to docker-compose                     | **Done** | `docker compose up` starts all services without extra steps. |
| A-18 | **S**  | Expose FastAPI router (or rename gateway)               | **Done** | File renamed to `backend/gateway.py`; docs updated. |
| S-09 | **S**  | JWT secret rotation & path-traversal tests               | **Done** | Added rotation guide and ensured path traversal test. |
| Q-04 | **S**  | Coverage reporting & badges                             | **Done** | CI runs coverage, uploads to Codecov, README badge added. |
| R-03 | **C**  | Sync version & CHANGELOG                                 | **Done** | Release workflow bumps version and changelog on tags. |
| F-07 | **C**  | Migrate FE to TypeScript                                 | **Done** | React code fully in TS; `pnpm typecheck` validates types. |
| T-05 | **C**  | Solver edge-case unit tests                              | **Done** | Stress cases for ill-conditioned graphs; CI green. |

| D-22 | **S**  | Deployment automation (CPU & GPU images)               | **Done** | Release workflow builds and pushes Docker images |
| D-23 | **S**  | Scalability benchmarking                              | **Done** | Benchmark script and tuning docs |
| F-08 | **C**  | Advanced front-end features                            | **Done** | Offline queue + settings page |
| F-09 | **C**  | Community example library                             | **Done** | Gallery of prompts and builds |
| F-10 | **C**  | Multi-language support                                | **Removed** | Interface fixed to English; no further translation work planned |
| B-33 | **S**  | Cloud infrastructure templates                       | **Done** | Terraform sample for AWS App Runner |
| B-34 | **S**  | Automated UI regression tests                        | **Done** | Cypress setup and basic PWA flow test |
| F-11 | **C**  | Real-time collaboration via WebSocket                | **Done** | `lego-gpt-collab` server |
| B-35 | **S**  | Custom model checkpoint support                      | **Done** | `LEGOGPT_MODEL` env var |
| F-12 | **C**  | Accessibility polish                                 | **Done** | ARIA labels & keyboard nav |
| F-13 | **C**  | Collaborative undo/redo                              | **Done** | `/undo` and `/redo` commands |
| F-14 | **C**  | Push subscription toggle                             | **Done** | Settings page button |
| F-15 | **C**  | Expanded example library                             | **Done** | More sample prompts |
| F-16 | **C**  | Automated front-end setup                           | **Done** | Dev container installs packages via setup script |
| F-17 | **C**  | Presence indicator in collaboration demo            | **Done** | Server broadcasts peer count; UI shows connected collaborators |
| B-36 | **S**  | Example submission pipeline                        | **Done** | `/submit_example` endpoint stores community prompts |
| B-37 | **S**  | Build progress events                              | **Done** | SSE endpoint `/progress/<job_id>` |
| F-18 | **S**  | Automatic example tagging                         | **Done** | Tags are generated when approving submissions |
| F-19 | **S**  | Example search and filter                        | **Done** | Gallery filters examples by tag or search text |
| F-20 | **S**  | Example comments                                | **Done** | Users can post comments via the API |
| F-21 | **S**  | Social sharing links                            | **Done** | Share buttons on examples and builds |
| F-22 | **S**  | Advanced build instructions                     | **Done** | PDF export lists used parts |
| F-23 | **S**  | Push notification opt-in                        | **Done** | One-time prompt on first visit |
| F-24 | **S**  | Admin analytics dashboard                        | **Done** | Metrics endpoint and dashboard page |
| F-25 | **S**  | Comment notifications                             | **Done** | Email sent on new example comments |
| F-26 | **S**  | Submission reporting                             | **Done** | Users can flag examples for admin review |
| F-27 | **S**  | Rate-limit metrics                               | **Done** | Token usage and limit hits shown in analytics |
| F-28 | **C**  | CLI config token                                 | **Done** | CLI reads token from `~/.lego-gpt` |
| F-29 | **S**  | Mobile performance audit                         | **Done** | Lighthouse CI checks performance budgets |
| F-30 | **S**  | Comment moderation tools                         | **Done** | Admins can delete comments and ban users |
| F-31 | **S**  | Example report review UI                        | **Done** | Clear flagged examples in admin dashboard |
| F-32 | **S**  | Token usage graphs                              | **Done** | Dashboard charts request and rate-limit history |
| F-33 | **S**  | Offline CLI usage                               | **Done** | CLI queues requests offline and replays later |
| F-34 | **S**  | Advanced performance budgets                    | **Done** | Lighthouse CI checks accessibility & best practices |
| F-35 | **S**  | Federated comment moderation                    | **Done** | Sync banned-user lists via new CLI |
| F-36 | **S**  | Persistent offline queue                       | **Done** | Front-end and CLI store pending requests across sessions |
| F-37 | **S**  | Issue triage guidelines                        | **Done** | Documented weekly review and labelling process |
| F-38 | **S**  | Container vulnerability scanning               | **Open** | Planned Trivy integration deferred |
| F-39 | **S**  | Long-term support policy                       | **Done** | Security updates provided for 12 months |
| F-40 | **M**  | FastAPI gateway refactor (Epic E‑07)           | **Open** | Sprints 88‑93 migrate the gateway to FastAPI |
### Legend
* **Pri** – MoSCoW priority (**M**ust, **S**hould, **C**ould, **W**on’t-Have-Now).
* **Status** – Open / WIP / Blocked / Done.

_Last updated 2025-08-17_
