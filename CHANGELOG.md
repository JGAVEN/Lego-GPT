
## Unreleased
### Added
* **Photo‑based brick inventory detection** feature (YOLOv8 detector, `/detect_inventory` API, front‑end scan workflow).
* `/detect_inventory` endpoint implementation with stub worker and tests.
* Declared `ortools` dependency in `backend/pyproject.toml`.
* `inventory_filter` payload option for `/generate` to limit bricks per request.

### Changed
* Updated architecture and backlog documentation.

### Fixed
* _None yet_

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
  - Auto‑loader selecting OR‑Tools → Gurobi (if licensed) → stub
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