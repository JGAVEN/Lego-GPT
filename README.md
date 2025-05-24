
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

## 2. What’s New (2025-06-08)
| Change | Impact |
|--------|--------|
| 🔄 **Open-source solver** – switched to **OR-Tools 9.10 + HiGHS**. | Runs licence-free everywhere (local dev, CI, containers). |
| 🔌 **Auto-loader** picks the first available backend (OR-Tools or a stub if missing). | Seamless fallback; no code changes needed. |
| 🩹 **Solver shim** monkey-patches the CMU call-site (`stability_score`). | Upstream sub-module remains untouched. |
| 🔐 **JWT auth + rate limit** on `/generate` | Prevents abuse; set `JWT_SECRET` and `RATE_LIMIT` |
| 🧩 **Connectivity filter** in solver | Removes brick clusters not connected to the ground |
| 🖼️ **Three.js LDraw viewer** | Interactive 3-D view if `.ldr` output is available |
| 🌐 **AR Quick-Look export** | `.gltf` file for iOS AR viewer |
| 📦 **Inventory filter** | Limits brick counts using `BRICK_INVENTORY` JSON or per-request `inventory_filter` |
| 🆕 **Photo‑based brick inventory detection** – YOLOv8 detector + `/detect_inventory` API | Scan your loose bricks and generate builds you can actually build |
| 🛡️ **Static file handler sanitized** | Blocks path traversal in `/static` requests |
| 🆕 **Console scripts** for API and workers (`lego-gpt-server`, `lego-gpt-worker`, `lego-detect-worker`) | Easier local development & Docker entrypoints; workers accept `--redis-url` and `--version` |
| 🛠️ **Ruff linting** for backend code | Consistent style via `ruff check` locally and in CI |
| 🌍 **CORS configuration** via `--cors-origins` | Allows custom `Access-Control-Allow-Origin` |
| 🔗 **Static URL prefix** configurable | Set `STATIC_URL_PREFIX` to point asset links at a CDN |
| ☁️ **S3/R2 uploads** | Set `S3_BUCKET` and `S3_URL_PREFIX` to host assets in the cloud |

&nbsp;

## 3. Quick-Start (Dev)

```bash
# Clone and set up
git clone https://github.com/JGAVEN/Lego-GPT.git
cd Lego-GPT

# Install pnpm (requires Node.js)
npm install -g pnpm@10.5.2

# Install front-end dependencies.
# The script installs from the local pnpm store if possible and fetches from
# the registry when online. Run it once with network access.
# Running it offline before the store is populated will print instructions
# to retry with network access. The script requires `pnpm` to be installed.
./scripts/setup_frontend.sh

# Install backend dependencies (including optional test tools)
python -m pip install --editable ./backend[test]
# The dev container's setup script runs this automatically.

# Start Redis (local or Docker)
# docker run -p 6379:6379 -d redis:7
# Optionally set the Redis URL for server and workers
export REDIS_URL=redis://localhost:6379/0

# Launch the RQ worker in one terminal
# ``--redis-url`` overrides the REDIS_URL env var
# Optional ``--queue`` overrides the QUEUE_NAME env var
export QUEUE_NAME=legogpt
lego-gpt-worker --redis-url "$REDIS_URL" --queue "$QUEUE_NAME" \
  --log-level INFO
# Launch the detector worker in another
lego-detect-worker --redis-url "$REDIS_URL" --queue "$QUEUE_NAME" \
  --model detector/model.pt \
  --log-level INFO
# Append ``--version`` to either worker command to print the version and exit

# Launch the API server in another
export JWT_SECRET=mysecret         # auth secret
export BRICK_INVENTORY=backend/inventory.json  # optional inventory
export DETECTOR_MODEL=detector/model.pt       # optional YOLOv8 weights (or pass --model)
# ``--jwt-secret``, ``--redis-url`` and ``--rate-limit`` override the
# corresponding environment variables. Use ``--log-level`` or ``LOG_LEVEL``
# to control verbosity for server and workers.
lego-gpt-server \
  --host 0.0.0.0 \
  --port 8000 \
  --redis-url "$REDIS_URL" \
  --jwt-secret "$JWT_SECRET" \
  --rate-limit 5 \
  --queue "$QUEUE_NAME" \
  --log-level INFO              # http://localhost:8000/health
# The `--host` and `--port` options can also be provided via `HOST` and
# `PORT` environment variables. Use `--version` to print the backend version
# and exit.
# Generated assets are written to `backend/static/{uuid}/` by default.
# Pass ``--static-root <dir>`` or set the ``STATIC_ROOT`` environment
# variable to override the directory. ``STATIC_URL_PREFIX`` customises
# the URL prefix returned in API responses (default: ``/static``).
# Set ``CORS_ORIGINS`` or pass ``--cors-origins <origins>`` to control the
# ``Access-Control-Allow-Origin`` header.
# Set ``S3_BUCKET`` and optional ``S3_URL_PREFIX`` to upload assets to S3/R2.

# Generate a JWT for requests
python scripts/generate_jwt.py --secret mysecret --sub dev

# Start the front-end PWA
pnpm --dir frontend run dev    # http://localhost:5173
# Lint UI code (skips if dependencies are missing)
pnpm --dir frontend run lint
# Lint backend code
ruff check backend detector
```

### Pre-commit Hooks
Install hooks with `pre-commit install` to automatically run `ruff` on each
commit. The configuration lives in `.pre-commit-config.yaml`.

Run `./scripts/run_tests.sh` to lint and test in one step.

The Vite dev server proxies `/generate`, `/detect_inventory`, and `/static`
requests to `http://localhost:8000` so the PWA works against your local backend
without CORS issues.

### Docker Compose

Alternatively, start the API server along with the generation and detector
workers in Docker containers. The dev Dockerfiles install all backend
dependencies so the stack works out‑of‑the‑box:

```bash
docker compose up --build
```

This spins up the API server, a generation worker and the detector worker.

The API will be available at http://localhost:8000/health.
The `/health` endpoint responds with `{ "ok": true, "version": "x.y.z" }` so you
can verify the backend version.

### Train the Brick Detector

Fine‑tune the YOLOv8 model when you have a labelled dataset. The
`lego-detect-train` console script wraps the `ultralytics` training API:

```bash
lego-detect-train data.yaml --epochs 100 --out detector/model.pt
```

The resulting weights file can then be referenced via the `DETECTOR_MODEL`
environment variable when running the detector worker.

> **Prerequisites**
> * Python 3.11+
> * Node.js 20+
> * pnpm package manager
> * Optional: `boto3` for S3 uploads

&nbsp;

## 4. Repository Layout

```text
backend/            Simple HTTP API + solver shim
└── solver/         ILP interface and OR-Tools backend
docs/               Project docs  (ARCHITECTURE, PROJECT_BACKLOG, CHANGELOG…)
frontend/           React + Vite PWA scaffold
vendor/legogpt/     Vendored CMU LegoGPT library
detector/           Brick-detector micro-service worker
docker-compose.yml  Dev stack (server + workers)
```

&nbsp;

## 5. API Contract

`GET /health` returns `{ "ok": true, "version": "x.y.z" }` and can be used to
verify that the backend is running.

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

`POST /detect_inventory` expects `{ "image": "<base64>" }` with a **valid**
base64 string and returns `{ "job_id": "xyz" }`. Invalid base64 yields
`HTTP 400`. Poll
`GET /detect_inventory/{job_id}` for the result:

```json
{ "brick_counts": { "3001.DAT": 2 } }
```

Use the counts as the `inventory_filter` in `/generate` requests.

Default rate limit is `5` generate requests per token per minute (configurable via `RATE_LIMIT`).

&nbsp;

## 6. Contributing

1. **One atomic branch per ticket** (`feature/<ticket-slug>`).
2. Follow `docs/PROJECT_BACKLOG.md` for ticket IDs and size.
3. Front-end dependencies are installed via `scripts/setup_frontend.sh`.
   The script first attempts an offline install and fetches from the registry if needed.
   Run it once with network access (`pnpm install --dir frontend` works too) so
   future lints and dev builds work offline.
   Running it before this first networked install will show a message
   explaining that the pnpm store is missing.
   Run `pnpm --dir frontend run lint` after editing UI code. The command skips if
   dependencies are missing.
4. Run `python -m unittest discover -v` before pushing. The test suite uses
   Python's built-in `unittest` module. `pytest` is optional and works too.
5. Update `docs/CHANGELOG.md` after each merge to `main`.

See `docs/CONTRIBUTING.md` for full workflow, coding style, and commit-message
conventions.

&nbsp;

## 7. Licence

| Component | Licence |
|-----------|---------|
| CMU LegoGPT library (`vendor/legogpt/…`) | CMU licence (see `vendor/legogpt/LICENSE`) |
| All new code in this repo (backend, solver, front-end) | **MIT** |

Lego® is a trademark of the LEGO Group, which does not sponsor or endorse this project.

