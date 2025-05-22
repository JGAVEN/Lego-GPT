
# Changelog

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
