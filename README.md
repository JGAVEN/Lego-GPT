
# Lego GPT

Generate buildable **LEGO®** creations directly from your browser.

---

## 1. Overview  
Lego GPT pairs the CMU **LegoGPT** Llama-3 1B model with a small **HTTP** server
and a **React + Three.js** progressive-web-app (PWA).
The model converts natural-language prompts into **LDraw** brick assemblies,
renders a PNG preview, and serves the `.ldr` file for 3-D manipulation or
real-life building.

&nbsp;

## 2. What’s New (2025-05-17)
| Change | Impact |
|--------|--------|
| 🔄 **Open-source solver** – replaced proprietary Gurobi MIP with **OR-Tools 9.10 + HiGHS**. | Runs licence-free everywhere (local dev, CI, containers). |
| 🔌 **Auto-loader** picks the first available backend (OR-Tools → Gurobi if licence exists). | Seamless fallback; no code changes needed. |
| 🩹 **Solver shim** monkey-patches the CMU call-site (`stability_score`). | Upstream sub-module remains untouched. |

&nbsp;

## 3. Quick-Start (Dev)

```bash
# Clone and set up
git clone https://github.com/JGAVEN/Lego-GPT.git
cd Lego-GPT

# Start Redis (local or Docker)
# docker run -p 6379:6379 -d redis:7

# Launch the RQ worker in one terminal
python backend/worker.py

# Launch the API server in another
python backend/server.py    # http://localhost:8000/health
```

> **Prerequisites**
> * Python 3.11+

&nbsp;

## 4. Repository Layout

```text
backend/            Simple HTTP API + solver shim
└── solver/         ILP interface and OR-Tools backend
docs/               Project docs  (ARCHITECTURE, BACKLOG, CHANGELOG…)
frontend/           React + Vite PWA scaffold
vendor/legogpt/     Vendored CMU LegoGPT library
docker-compose.yml  Dev stack (backend only for now)
```

&nbsp;

## 5. API Contract

`POST /generate` accepts a JSON body:

```json
{ "prompt": "text description", "seed": 42 }
```

It returns a job handle:

```json
{ "job_id": "c0ffee" }
```

Poll the job via `GET /generate/{job_id}` to receive the asset links:

```json
{
  "png_url": "/static/{uuid}/preview.png",
  "ldr_url": "/static/{uuid}/model.ldr",  // may be null
  "brick_counts": { "Brick 2 x 4": 12 }
}
```

The `png_url` can be shown directly in an `<img>` tag. The optional
`ldr_url` is for future Three.js viewing.

&nbsp;

## 6. Contributing

1. **One atomic branch per ticket** (`feature/<ticket-slug>`).
2. Follow `docs/BACKLOG.md` for ticket IDs and size.
3. Install front-end dependencies with `pnpm install` (run inside `frontend/`)
   before running `npm run lint`.
4. Run `python -m unittest discover -v` before pushing. The test suite uses
   Python's built-in `unittest` module—no need for `pytest`.
5. Update `docs/CHANGELOG.md` after each merge to `main`.

See `docs/CONTRIBUTING.md` for full workflow, coding style, and commit-message
conventions.

&nbsp;

## 7. Licence

| Component | Licence |
|-----------|---------|
| CMU LegoGPT library (`vendor/legogpt/…`) | CMU licence (see `vendor/legogpt/LICENSE`) |
| All new code in this repo (backend, solver, front-end) | **MIT** |

Lego® is a trademark of the LEGO Group, which does not sponsor or endorse this
project.
