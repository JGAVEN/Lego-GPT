# Sprint Plan

This document outlines the next five logical sprints for the project.

## Sprint 1 – Docker Compose Redis service (completed)
* Add a `redis` service to `docker-compose.yml` and `backend/docker-compose.yml`.
* Update README instructions and mark backlog item D‑21 as **Done**.

## Sprint 2 – Expose FastAPI router (completed)
* Renamed `backend/server.py` to `backend/gateway.py` and updated docs/tests.

## Sprint 3 – JWT secret rotation & path traversal tests (completed)
* Documented token rotation procedure in `docs/TOKEN_ROTATION.md`.
* Added/verified unit test blocking `../` escapes.

## Sprint 4 – Coverage reporting (completed)
* Added coverage run in CI and Codecov upload.
* README shows the Codecov badge.

## Sprint 5 – Version & changelog automation (completed)
* Created `scripts/bump_version.py` and release workflow for tag-based bumps.
