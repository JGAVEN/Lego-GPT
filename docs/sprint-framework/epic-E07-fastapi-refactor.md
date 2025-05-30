# Epic E-07 · FastAPI Gateway Refactor & Deployment

> Goal: Replace the current `backend/gateway.py` (`http.server`) with a
> FastAPI app that offers automatic docs, request validation, middleware,
> rate-limiting, and future-proof routing.

---

## MVP Defaults

| Setting | Value |
|---------|-------|
| Concurrency | Sync helpers wrapped with `run_in_threadpool` |
| Auth | Single bearer token from `API_TOKEN` env var |
| CORS | `https://lego-gpt-frontend.onrender.com`, `http://localhost:5173`, `https://*.your-custom-domain.com` |
| Rate-limit | 60 req/min/IP via `slowapi` |
| Legacy gateway | Served under `/v0/*` for 30 days |

---

## Sprint schedule (6 × 1‑week)

| Sprint | Objective | Exit Criteria |
|--------|-----------|---------------|
| **S7‑1** Scaffold FastAPI app | `backend/api.py` with `/health` OK locally |
| **S7‑2** Migrate GET routes | `/metrics`, `/metrics_prom`, `/history` + tests |
| **S7‑3** Migrate POST routes | `/generate`, `/detect_inventory`, misc helpers |
| **S7‑4** Middleware & security | CORS, bearer‑token auth stub, rate‑limit |
| **S7‑5** CI/CD & Render rollout | `render.yaml` updated, blue/green deploy |
| **S7‑6** Docs & monitoring | Polished `/docs`, Prometheus metrics, README |

---

## Sprint backlog

### S7‑1 · Scaffold

| Story | Task list |
|-------|-----------|
| **S7‑1‑001** Create FastAPI skeleton | *a)* Add `backend/api.py` with:<br>&nbsp;&nbsp;```python
from fastapi import FastAPI
from starlette.concurrency import run_in_threadpool
app = FastAPI(title="Lego‑GPT API")

@app.get("/health")
async def health():
    return {"status": "ok"}
```<br>*b)* Ensure `backend/__init__.py` exists. |
| **S7‑1‑002** Local dev commands | *a)* Add Makefile target: `make dev-api` → `uvicorn backend.api:app --reload`.<br>*b)* VS Code `launch.json` entry. |
| **S7‑1‑003** Dependencies | Append to `backend/requirements.txt`:<br>`fastapi
uvicorn[standard]
slowapi` |

*(Backlog for S7‑2 … S7‑6 continues in repo document.)*

---

## CI / Render adjustments

* **render.yaml** (service *lego‑gpt‑api*):
  ```yaml
  rootDir: backend
  startCommand: uvicorn api:app --host 0.0.0.0 --port $PORT
  ```
  A second service `lego-gpt-api-blue` is defined but kept disabled to allow
  blue/green rollouts.
* **.github/workflows/ci.yml**:  
  * run `pytest`  
  * run smoke test: `uvicorn backend.api:app --port 9999 --lifespan on --log-level warning` for 5 s.

---

## Deprecation notice

* Legacy gateway mounted under `/v0/*` for 30 days, then removed.

---

_End of file_
