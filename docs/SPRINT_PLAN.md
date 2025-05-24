# Sprint Plan

This document outlines the next five logical sprints for the project.

## Sprint 1 – Docker Compose Redis service (completed)
* Add a `redis` service to `docker-compose.yml` and `backend/docker-compose.yml`.
* Update README instructions and mark backlog item D‑21 as **Done**.

## Sprint 2 – Expose FastAPI router
* Surface a reusable `APIRouter` in `backend/api.py` or rename `server.py` to clarify that it acts as the gateway.
* Update documentation accordingly.

## Sprint 3 – JWT secret rotation & path traversal tests
* Document token rotation procedure.
* Add unit tests ensuring the static file handler rejects `../` escapes.

## Sprint 4 – Coverage reporting
* Integrate `pytest-cov` in the test workflow.
* Upload coverage to Codecov and show a badge in the README.

## Sprint 5 – Version & changelog automation
* Add a release workflow that bumps the version and updates the changelog on tags.
