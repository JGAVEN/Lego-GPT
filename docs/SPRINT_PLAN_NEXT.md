# Next Sprint Plan

> **Note**: The software remains English-only.

The next six sprints implement **Epic E-07 – FastAPI Gateway Refactor**.

## Sprint 88 – FastAPI scaffold
* Add `backend/api.py` with a `/health` route and dev command.

## Sprint 89 – GET route migration
* Move `/metrics`, `/metrics_prom` and `/history` with tests.

## Sprint 90 – POST route migration
* Refactor `/generate` and `/detect_inventory` for FastAPI.

## Sprint 91 – Middleware & security
* Enable CORS, bearer-token auth stub and rate limiting.

## Sprint 92 – CI/CD & Render rollout
* Update `render.yaml` and deploy with blue/green strategy.

## Sprint 93 – Docs & monitoring
* Polish `/docs`, expose Prometheus metrics and update README.
