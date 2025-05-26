## [0.5.62] – 2025-08-09
### Added
- `lego-gpt-cli completion` outputs shell completion scripts.
- Tutorial overlay guides first-time PWA users.
- `/metrics_prom` endpoint exposes Prometheus metrics.
- `lego-gpt-translate` CLI translates example prompts.
- Helm chart provided under `infra/helm`.
### Changed
- Backend version bumped to 0.5.62.

## [0.5.61] – 2025-08-08
### Added
- `lego-gpt-analytics` CLI exports metrics history to CSV.
- Dark mode toggle remembers the chosen theme.
- YAML configuration loaded via `LEGOGPT_CONFIG` or `--config`.
- CLI loads plugins from `~/.lego-gpt/plugins`.
- API server runs scheduled cleanup of old assets.
### Changed
- Backend version bumped to 0.5.61.

## [0.5.46] – 2025-07-28
### Added
* Example submission endpoint `/submit_example`.
* SSE progress streaming via `/progress/<job_id>`.
### Changed
* Backend version bumped to 0.5.46.

## [0.5.47] – 2025-07-29
### Added
* `lego-gpt-review` CLI for approving community examples.
* `lego-gpt-cli` streams build progress via SSE.

## [0.5.48] – 2025-08-01
### Added
* Automatic example tagging when approving submissions.
* Gallery search box and tag filter for community examples.
### Changed
* Backend version bumped to 0.5.48.

## [0.5.49] – 2025-08-02
### Added
* Example comments and social sharing buttons in the PWA.
* PDF export now lists used parts.
* Push notification opt-in prompt.
* Admin metrics dashboard and `/metrics` endpoint.
### Changed
* Backend version bumped to 0.5.49.

## [0.5.50] – 2025-08-03
### Added
* Email notifications for new example comments.
### Changed
* Backend version bumped to 0.5.50.

## [0.5.51] – 2025-08-04
### Added
* Distributed moderation queue using Redis.
* Account linking via one-time codes.
* Notification preferences stored per user.
* `lego-gpt-examples` import/export tool.
### Changed
* Worker jobs retry automatically and `/health` reports Redis status.
* Backend version bumped to 0.5.51.

## [0.5.52] – 2025-08-05
### Added
* Submission reporting via `/report` endpoint.
* Rate-limit metrics tracked in analytics.
* `lego-gpt-cli` loads tokens from `~/.lego-gpt`.
* Lighthouse CI performance budget check.
* Comment moderation endpoints for deleting comments and banning users.
### Changed
* Backend version bumped to 0.5.52.

## [0.5.53] – 2025-08-06
### Added
* Admin report review page for flagged examples.
* Metrics dashboard shows token usage graphs.
* CLI queues requests offline and replays them later.
* Accessibility and best-practices budgets checked in CI.
* `lego-gpt-sync-bans` CLI syncs banned-user lists.
### Changed
* Backend version bumped to 0.5.53.

## [0.5.54] – 2025-08-07
### Added
* Persistent offline queue for front-end and CLI.
### Changed
* Backend version bumped to 0.5.54.

## [0.5.45] – 2025-07-27
### Added
* Presence indicator shows connected collaborators in real time.
### Changed
* Backend version bumped to 0.5.45.

## [0.5.42] – 2025-07-15
### Added
* Offline collaboration queue with IndexedDB.
* Push notifications triggered by collaboration events.
* Demo page showcasing real-time editing.

## [0.5.43] – 2025-07-25
### Added
* Collaborative undo/redo commands in the WebSocket server.
* Push notification toggle in the settings page.
* Expanded community example gallery.

## [0.5.44] – 2025-07-26
### Added
* Dev container setup installs front-end dependencies via `scripts/setup_frontend.sh`.
### Changed
* `run_tests.sh` now attempts to install front-end packages if missing.

## [0.5.41] – 2025-07-02
### Added
* `lego-gpt-collab` WebSocket server for real-time collaboration.
* Environment variable `LEGOGPT_MODEL` to load custom checkpoints.
* Additional ARIA labels improve accessibility in the PWA.

## [0.5.40] – 2025-06-25
### Added
* CI now runs a lightweight scalability benchmark using a stub server.

## [0.5.39] – 2025-06-24
### Changed
* `lint_frontend.js` no longer tries to install packages offline; it simply
  prints a brief message when dependencies are missing.

## [0.5.38] – 2025-06-23
### Added
* Install prompt and touch-friendly viewer.
### Changed
* Backend package version bumped to 0.5.38.

## [0.5.37] – 2025-06-22
### Added
* Offline request queue with automatic processing when back online.
* Settings page to manage cached results and queued jobs.
### Changed
* Backend package version bumped to 0.5.37.

## [0.5.36] – 2025-06-22
### Added
* Benchmark script `benchmark_scalability.py` and scalability docs.
### Changed
* Backend package version bumped to 0.5.36.

## [0.5.35] – 2025-06-22
### Added
* Production Docker images for CPU and GPU targets.
### Changed
* Backend package version bumped to 0.5.35.

## [0.5.34] – 2025-06-21
### Added
* CLI integration tests covering batch and progress features.
### Changed
* Backend package version bumped to 0.5.34.

## [0.5.33] – 2025-05-26
### Changed
* Documentation clarifies offline front-end lint behavior.
* Backend package version bumped to 0.5.33.

## [0.5.32] – 2025-05-25
### Added
* Offline mode improvements: IndexedDB caching for API responses.
* Service worker caches preview images for offline viewing.
### Changed
* Backend package version bumped to 0.5.32.

## [0.5.31] – 2025-05-24
### Added
* Training Dockerfile (`detector/Dockerfile.train`) and helper script `scripts/train_detector.sh`.
* Documentation of the detector dataset format.
### Changed
* Backend package version bumped to 0.5.31.

## [0.5.30] – 2025-06-19
### Added
* Solver edge-case unit tests covering loops and multi-level overhang scenarios.
### Changed
* Backend package version bumped to 0.5.30.

## [0.5.29] – 2025-06-18
### Added
* `pnpm typecheck` script ensures the TypeScript front-end builds cleanly.
### Changed
* Backend package version bumped to 0.5.29.

## [0.5.28] – 2025-06-17
### Added
* Redis service in `docker-compose.yml`.
### Changed
* Backend package version bumped to 0.5.28.

## [0.5.27] – 2025-06-16
### Added
* Front-end `VITE_API_URL` configuration with example env file.
* `--out-dir` option for `lego-gpt-cli generate` to download assets.
### Changed
* Backend package version bumped to 0.5.27.

## [0.5.26] – 2025-06-15
### Added
* Logging to file via `--log-file` and `LOG_FILE`.
### Changed
* Backend package version bumped to 0.5.26.

## [0.5.25] – 2025-06-15
### Added
* `lego-gpt-export` CLI converts `.ldr` to `.gltf`.
### Changed
* Backend package version bumped to 0.5.25.

## [0.5.24] – 2025-06-15
### Added
* `.env` loading for `lego-gpt-cli`.
### Changed
* Backend package version bumped to 0.5.24.

## [0.5.23] – 2025-06-15
### Added
* `--inventory` option for `lego-gpt-cli` to send brick counts.
### Changed
* Backend package version bumped to 0.5.23.

## [0.5.22] – 2025-06-14
### Added
* `lego-gpt-token` console script for JWT generation.
* `ORTOOLS_ENGINE` env var and `--solver-engine` worker option.
### Changed
* Backend package version bumped to 0.5.22.

## [0.5.21] – 2025-06-13
### Added
* `--dry-run` option for `lego-gpt-cleanup`.
### Changed
* Backend package version bumped to 0.5.21.

## [0.5.18] – 2025-06-10
### Added
* `--version` flag for `lego-gpt-cli` and accompanying unit tests.
### Changed
* Backend package version bumped to 0.5.18.

## [0.5.19] – 2025-06-11
### Added
* `.env` configuration support via optional `python-dotenv`.
* Example `.env.example` file.
### Changed
* Backend package version bumped to 0.5.19.

## [0.5.20] – 2025-06-12
### Added
* `lego-gpt-cleanup` script removes old static assets.
### Changed
* Backend package version bumped to 0.5.20.

## [0.5.17] – 2025-06-09
### Added
* `lego-gpt-cli` command-line client for interacting with the API.
### Changed
* Backend package version bumped to 0.5.17.

## [0.5.16] – 2025-06-09
### Added
* `ruff` included in `backend[test]` extras for local linting.
### Changed
* Backend package version bumped to 0.5.16.

## [0.5.15] – 2025-06-08
### Added
* Optional S3/R2 upload via `S3_BUCKET` and `S3_URL_PREFIX`.
* `boto3` optional dependency (`s3` extra).
### Changed
* Backend package version bumped to 0.5.15.

## [0.5.14] – 2025-06-06
### Added
* `--cors-origins` option and `CORS_ORIGINS` env var configure CORS.
* Static `.gltf` files served with `model/gltf+json` content type.
* OPTIONS requests include CORS headers.
### Changed
* Backend package version bumped to 0.5.13.

## [0.5.13] – 2025-06-05
### Added
* `--static-root` option for `lego-gpt-server` to override the output directory.
* Documentation updated with new server option.
* Unit test covers the CLI parsing of `--static-root`.
* `--model` option for `lego-detect-worker` sets the YOLOv8 weights path.
* ``--log-level`` option and ``LOG_LEVEL`` env var configure logging for server
  and workers.
* Added `.pre-commit-config.yaml` for automatic `ruff` checks.
* `scripts/run_tests.sh` runs linting and tests.

### Changed
* Project version bumped to 0.5.13.

## [0.5.12] – 2025-06-04
### Added
* `--version` flag for `lego-gpt-worker` and `lego-detect-worker`.
* Unit tests covering worker CLI options.

### Changed
* Project version bumped to 0.5.12.

## [0.5.11] – 2025-06-03
### Added
* Unit test covering server CLI options.

### Changed
* Project version bumped to 0.5.11.

## [0.5.10] – 2025-06-02
### Added
* CLI options `--redis-url`, `--jwt-secret` and `--rate-limit` for `lego-gpt-server`.

### Changed
* Documentation updated with new server options.
* Project version bumped to 0.5.10.

## [0.5.9] – 2025-06-01
### Added
* `ruff` linting configuration in `pyproject.toml`.
* CI workflow runs `ruff` for backend and detector code.

### Changed
* Documentation updated to reference running `ruff` locally.
* Project version bumped to 0.5.9.

## [0.5.8] – 2025-05-31
### Added
* `QUEUE_NAME` env var and `--queue` option allow custom RQ queue names for
  server and workers.
### Changed
* Project version bumped to 0.5.8.

## [0.5.7] – 2025-05-31
### Added
* Docker Compose stack now includes a dedicated generation worker.
* Docker images use the new console scripts as default entrypoints.
### Changed
* Project version bumped to 0.5.7.

## [0.5.6] – 2025-05-31
### Added
* `--redis-url` option for `lego-gpt-worker` and `lego-detect-worker`.
### Changed
* Project version bumped to 0.5.6.

## [0.5.5] – 2025-05-31
### Added
* `STATIC_ROOT` environment variable allows overriding the default
  `backend/static` directory.
### Changed
* Project version bumped to 0.5.5.

## [0.5.4] – 2025-05-31
### Added
* `lego-detect-train` script to fine-tune the YOLOv8 brick detector.
### Changed
* Project version bumped to 0.5.4.

## [0.5.3] – 2025-05-30
### Added
* Dev container setup installs backend dependencies including fakeredis for tests.
### Changed
* Static file path constant moved to `backend` package for consistency.
## [0.5.2] – 2025-05-29
### Added
* `lint_frontend.js` skips UI lint when dependencies are missing offline.


## [0.5.1] – 2025-05-28
### Added
* Console scripts `lego-gpt-server`, `lego-gpt-worker` and `lego-detect-worker`.
  Documentation updated to show their usage.

## [0.5.0] – 2025-05-27
### Added
* **Photo‑based brick inventory detection** feature (YOLOv8 detector, `/detect_inventory` API, front‑end scan workflow).
* `/detect_inventory` endpoint implementation with stub worker and tests.
* Declared `ortools` dependency in `backend/pyproject.toml`.
* `inventory_filter` payload option for `/generate` to limit bricks per request.
* React `InventoryScanner` component and `useDetectInventory` hook.
* Optional `fakeredis` dependency for running queue tests
* `detector/` micro-service and Dockerfile for inventory detection
* Optional `ultralytics` + `pillow` dependencies for real detection
* GitHub Actions CI lints front-end code with pnpm
* `scripts/setup_frontend.sh` installs UI dependencies for offline use
* Setup script now retries offline install before fetching packages
* Clearer message when the pnpm store lacks packages and no network is available
* `scripts/generate_jwt.py` helper for creating auth tokens
* `/health` endpoint now returns backend `version`
* `backend/gateway.py` accepts `--host` and `--port` CLI options (or `HOST`/`PORT` env vars)
* `backend/gateway.py` now supports `--version` to print the backend version
* `pytest` now works via `backend/tests/conftest.py` (optional)

### Changed
* Updated architecture and backlog documentation.
* Detector falls back to a stub unless `DETECTOR_MODEL` and `ultralytics` are available.
* `/detect_inventory` endpoint now validates base64 input server-side and
  returns `HTTP 400` if malformed.
* Pinned pnpm version to 10.5.2 for offline setup reliability.
* Dev Docker images now install backend dependencies automatically.
* `setup_frontend.sh` now exits if `pnpm` is missing and README quick-start
  installs pnpm before running the script.
* Vite dev server proxies `/detect_inventory` and `/static` to the backend for
  seamless development.

### Fixed
* CI installs pnpm before running front-end tests.
* Static file handler now blocks path traversal outside the `backend/static`
  directory.

# Changelog

## [0.3.9] – 2025-05-25
### Added
- Inventory filter trims brick counts using `BRICK_INVENTORY`.

## [0.3.8] – 2025-05-24
### Added
- AR Quick-Look export writes `model.gltf` alongside `.ldr` for iOS AR.

## [0.3.7] – 2025-05-23
### Added
- Setup script now installs front-end packages via PNPM before network access is disabled.
### Changed
- Docs updated to note automatic PNPM install and offline setup.

## [0.3.6] – 2025-05-23
### Added
- Three.js LDraw viewer component loads `.ldr` output when available.

## [0.3.5] – 2025-05-23
### Added
- Unit tests for JWT encode/decode helpers.
### Changed
- Solver shim documentation now reflects actual OR-Tools usage.

## [0.3.4] – 2025-05-23
### Added
- Solver now removes brick clusters not connected to the ground.

## [0.3.3] – 2025-05-23
### Added
- JWT authentication and per-token rate limiting on `/generate`.

## [0.3.2] – 2025-05-22
### Added
- Local `vendor/rq` and `vendor/redis` stubs allow tests to run offline.

## [0.3.1] – 2025-05-21
### Changed
- Docs now instruct running tests with `python -m unittest discover -v` as the
  project doesn’t rely on `pytest`.

## [0.3.0] – 2025-05-17
### Added
- **Open‑source solver scaffold** (`backend/solver/`) introducing:
  - `base.py` abstract `ILPSolver`
  - `ortools_solver.py` (OR‑Tools 9.10 + HiGHS backend)
  - Auto‑loader selecting OR‑Tools → stub when unavailable
- **Solver shim** (`backend/solver/shim.py`) that monkey‑patches
  `legogpt.stability_analysis.stability_score`.
- **Dependency**: added `ortools ^9.10` in `pyproject.toml`.
- Updated docs: README, ARCHITECTURE, BACKLOG to reflect solver swap.

### Fixed
- Removed missing `LegoLibrary` import in shim to restore passing tests.
 - Vendored `legogpt` library under `vendor/`.

## [0.2.0] – 2025‑05‑16
### Added
- `/generate` endpoint with mocked LegoGPT wrapper.
- Integration test `backend/tests/test_generate.py`.
- `pytest.ini` for import path.
- Front‑end scaffold (React + Vite + TS).
- Docker dev stack (Dockerfile.dev + docker-compose.yml).

### Fixed
- Dockerfile `COPY` paths.

## [0.1.0] – 2025‑05‑14
### Added
- Initial repository setup with docs, `.gitignore`, and backend `/health`.
