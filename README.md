
# Lego GPT

Generate buildable **LEGO®** creations directly from your browser.

---

## 1. Overview  
Lego GPT pairs the CMU **LegoGPT** Llama-3 1B model with a small **HTTP** server
and a **React + Three.js** progressive-web-app (PWA).
The model converts natural-language prompts into **LDraw** brick assemblies,
renders a PNG preview, and serves the `.ldr` file for 3-D manipulation or
real-life building via a built-in Three.js viewer.

&nbsp;

## 2. What’s New (2025-05-25)
| Change | Impact |
|--------|--------|
| 🔄 **Open-source solver** – replaced proprietary Gurobi MIP with **OR-Tools 9.10 + HiGHS**. | Runs licence-free everywhere (local dev, CI, containers). |
| 🔌 **Auto-loader** picks the first available backend (OR-Tools → Gurobi if licence exists). | Seamless fallback; no code changes needed. |
| 🩹 **Solver shim** monkey-patches the CMU call-site (`stability_score`). | Upstream sub-module remains untouched. |
| 🔐 **JWT auth + rate limit** on `/generate` | Prevents abuse; set `JWT_SECRET` and `RATE_LIMIT` |
| 🧩 **Connectivity filter** in solver | Removes brick clusters not connected to the ground |
| 🖼️ **Three.js LDraw viewer** | Interactive 3-D view if `.ldr` output is available |
| 🌐 **AR Quick-Look export** | `.gltf` file for iOS AR viewer |
| 📦 **Inventory filter** | Limits brick counts using `BRICK_INVENTORY` JSON or per-request `inventory_filter` |
| 🆕 **Photo‑based brick inventory detection** – YOLOv8 detector + `/detect_inventory` API | Scan your loose bricks and generate builds you can actually build |

&nbsp;

## 3. Quick-Start (Dev)

```bash
# Clone and set up
git clone https://github.com/JGAVEN/Lego-GPT.git
cd Lego-GPT

# Install backend dependencies (including optional test tools)
python -m pip install --editable ./backend[test]

# Start Redis (local or Docker)
# docker run -p 6379:6379 -d redis:7

# Launch the RQ worker in one terminal
python backend/worker.py
# Launch the detector worker in another
python detector/worker.py

# Launch the API server in another
export JWT_SECRET=mysecret         # auth secret
export BRICK_INVENTORY=backend/inventory.json  # optional inventory
python backend/server.py    # http://localhost:8000/health

# Generate a JWT for requests
python - <<'EOF'
from backend.auth import encode
print(encode({"sub": "dev"}, "mysecret"))
EOF

# Start the front-end PWA
pnpm --dir frontend run dev    # http://localhost:5173
```

> **Prerequisites**
> * Python 3.11+

&nbsp;

## 4. Repository Layout

```text
backend/            Simple HTTP API + solver shim
└── solver/         ILP interface and OR-Tools backend
docs/               Project docs  (ARCHITECTURE, PROJECT_BACKLOG, CHANGELOG…)
frontend/           React + Vite PWA scaffold
vendor/legogpt/     Vendored CMU LegoGPT library
detector/           Brick-detector micro-service worker
docker-compose.yml  Dev stack (backend + detector workers)
```

&nbsp;

## 5. API Contract

`POST /generate` requires an `Authorization: Bearer <token>` header and accepts a JSON body:

```json
{
  "prompt": "text description",
  "seed": 42,
  "inventory_filter": { "3001.DAT": 2 }  // optional
}
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
  "gltf_url": "/static/{uuid}/model.gltf", // AR Quick-Look
  "brick_counts": { "Brick 2 x 4": 12 }
}
```

The `png_url` can be shown directly in an `<img>` tag. If `ldr_url` is present,
pass it to the `LDrawViewer` React component for interactive viewing.

### Detect Brick Inventory

`POST /detect_inventory` expects `{ "image": "<base64>" }` and returns
`{ "job_id": "xyz" }`. Poll `GET /detect_inventory/{job_id}` for the result:

```json
{ "brick_counts": { "3001.DAT": 2 } }
```

Use the counts as the `inventory_filter` in `/generate` requests.

Default rate limit is `5` generate requests per token per minute (configurable via `RATE_LIMIT`).

&nbsp;

## 6. Contributing

1. **One atomic branch per ticket** (`feature/<ticket-slug>`).
2. Follow `docs/PROJECT_BACKLOG.md` for ticket IDs and size.
3. Front-end dependencies are installed automatically during setup via
   `pnpm fetch --dir frontend && pnpm install --offline --dir frontend`.
   Run `npm run lint` after editing UI code.
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