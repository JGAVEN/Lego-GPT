
# Lego GPT

Generate buildable **LEGO®** creations directly from your browser.

---

## 1. Overview  
Lego GPT pairs the CMU **LegoGPT** Llama-3 1B model with a **FastAPI** inference
gateway and a **React + Three.js** progressive-web-app (PWA).  
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
poetry install          # installs backend deps inc. OR-Tools

# Launch the backend (FastAPI + solver)
docker compose up       # http://localhost:8000/health

# Launch the front-end
cd frontend
pnpm install
pnpm dev                # http://localhost:5173
```

> **Prerequisites**
> * Docker ≥ 24, Docker Compose v2  
> * Python 3.12 (Poetry installs a venv)  
> * Node 18 + PNPM 8 for the React app  

&nbsp;

## 4. Repository Layout

```text
backend/            FastAPI API + solver shim
└── solver/         ILP interface and OR-Tools backend
docs/               Project docs  (ARCHITECTURE, BACKLOG, CHANGELOG…)
frontend/           React + Vite PWA scaffold
src/legogpt/        CMU LegoGPT model (git-submodule)
docker-compose.yml  Dev stack (backend only for now)
```

&nbsp;

## 5. Contributing

1. **One atomic branch per ticket** (`feature/<ticket-slug>`).  
2. Follow `docs/BACKLOG.md` for ticket IDs and size.  
3. Run `poetry run pytest` before pushing (CI currently checks the backend test suite).  
4. Update `docs/CHANGELOG.md` after each merge to `main`.  

See `docs/CONTRIBUTING.md` for full workflow, coding style, and commit-message
conventions.

&nbsp;

## 6. Licence

| Component | Licence |
|-----------|---------|
| CMU LegoGPT sub-module (`src/legogpt/…`) | CMU licence (see sub-module `LICENSE`) |
| All new code in this repo (backend, solver, front-end) | **MIT** |

Lego® is a trademark of the LEGO Group, which does not sponsor or endorse this
project.
