
# Lego GPT ![Coverage](https://codecov.io/gh/JGAVEN/Lego-GPT/branch/main/graph/badge.svg)

Generate buildable **LEGO®** creations directly from your browser. All interface text and prompts are in English only. The application does not include multilingual support and expects English input throughout.

---

## 1. Overview  
Lego GPT pairs the CMU **LegoGPT** Llama-3 1B model with a small **HTTP** server
and a **React + Three.js** progressive-web-app (PWA).
The model converts natural-language prompts into **LDraw** brick assemblies,
renders a PNG preview, and serves the `.ldr` file for 3-D manipulation or
real-life building via a built-in Three.js viewer.

&nbsp;

## 2. What’s New (2025-07-28)
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
| 📸 **Multiple inventory photos** | Combine several detected images into one project file |
| 🛡️ **Static file handler sanitized** | Blocks path traversal in `/static` requests |
| 🆕 **Console scripts** for API and workers (`lego-gpt-server`, `lego-gpt-worker`, `lego-detect-worker`) | Easier local development & Docker entrypoints; workers accept `--redis-url` and `--version` |
| 🆕 **Command-line client** (`lego-gpt-cli`) | Test the API from your terminal or CI |
| 🛠️ **Ruff linting** for backend code | Consistent style via `ruff check` locally and in CI |
| 🌍 **CORS configuration** via `--cors-origins` | Allows custom `Access-Control-Allow-Origin` |
| 🔗 **Static URL prefix** configurable | Set `STATIC_URL_PREFIX` to point asset links at a CDN |
| ☁️ **S3/R2 uploads** | Set `S3_BUCKET` and `S3_URL_PREFIX` to host assets in the cloud |
| 🆕 **CLI `--version` flag + tests** | `lego-gpt-cli --version` shows backend version; automated tests ensure it works |
| 🆕 **`--inventory` & `.env` support** | CLI loads env vars from `.env` and accepts `--inventory` JSON |
| 🆕 **Batch generation & progress** | Use `--file prompts.txt` and watch progress dots while waiting |
| 🧹 **Cleanup script** (`lego-gpt-cleanup`) | Remove old asset directories (use `--dry-run` to preview) |
| 🌐 **Collaboration server** (`lego-gpt-collab`) | WebSocket endpoint for real-time shared editing |
| 🆕 **Offline queue + settings** | Requests made offline are queued and cached results can be cleared in the settings page |
| 💾 **Persistent offline queue** | Pending requests survive reloads and CLI restarts |
| 🔔 **Push notifications** | Service worker shows notifications when collaborators edit a build |
| 📨 **Offline edit queue** | Collaboration messages are stored offline and synced on reconnect |
| ↩️ **Undo/redo support** | Collaborative sessions track history with `/undo` and `/redo` |
| 👥 **Presence indicator** | Shows connected collaborators in real time |
| 🔕 **Push toggle in settings** | Enable or disable Web Push with one click |
| 📱 **Install prompt & touch controls** | Add to Home Screen button and smoother mobile controls |
| 🖼️ **Community example gallery** | Browse shared prompts and load them with one click |
| ➕ **Expanded examples** | New sample prompts showcase model capabilities (see [docs/EXAMPLES.md](docs/EXAMPLES.md)) |
| ✉️ **Example submissions** | `/submit_example` endpoint stores community prompts |
| 📶 **Progress events** | `/progress/<job_id>` streams build updates via SSE |
| 🆕 **Submission review CLI** (`lego-gpt-review`) | Approve community examples from the command line |
| 🆕 **CLI progress streaming** | `lego-gpt-cli` shows live build progress via SSE |
| 🆕 **Automatic example tagging** | Submissions gain keyword tags during approval |
| 🆕 **Search & tag filter** | Gallery filters examples by text or tag |
| ⭐ **Rate & favourite examples** | Gallery stores star ratings and favourites locally |
| 💬 **Example comments** | Signed-in users can comment on community examples |
| 🔗 **Share buttons** | Share examples or generated builds via Web Share API |
| 📲 **Push opt-in** | One-time prompt to enable push notifications |
| 📊 **Admin analytics** | Simple dashboard with usage metrics |
| 📝 **Moderation dashboard** | Web interface to approve or reject community submissions |
| 💬 **Collaboration chat** | WebSocket chat messages in the collaboration demo |
| 📄 **PDF instructions** | Download simple build instructions with each model |
| 🌐 **Federated example search** | `/search_examples` aggregates remote galleries |
| 📱 **Mobile UI tweaks** | Larger touch targets on small screens |
| 🔑 **Admin roles** | JWT `role` claim gates moderation and metrics |
| 📡 **Metrics WebSocket** | `lego-gpt-metrics` streams live metrics |
| 📂 **Build history export** | `/history` endpoint provides past builds |
| 📥 **Distributed moderation queue** | Pending submissions stored in Redis and shared across instances |
| 🔗 **Account linking** | Sync build history across devices with one-time link codes |
| 🔔 **Notification preferences** | Settings page stores email and push options |
| 🗄️ **Example import/export** | Admin CLI can export and import community examples |
| 💪 **Worker resilience** | Jobs retry automatically; health check reports Redis status |
| 🚩 **Submission reporting** | Users can flag examples for admin review |
| 📈 **Rate-limit metrics** | Analytics charts token usage and limit hits |
| 🔐 **Improved CLI auth** | `lego-gpt-cli` reads token from `~/.lego-gpt` |
| 🚦 **Performance audit** | Lighthouse CI enforces PWA performance budgets |
| 🛡️ **Comment moderation tools** | Admins can delete comments and ban users |
| 📈 **Analytics export CLI** | `lego-gpt-analytics` outputs metrics history to CSV and can push it to a data warehouse |
| 🌓 **Dark mode toggle** | PWA remembers your light or dark theme preference |
| 🎨 **Accent colour picker** | Choose a custom UI highlight colour |
| 📝 **YAML config files** | Set `LEGOGPT_CONFIG` or `--config` to load settings |
| 🛠️ **Config generator** | `lego-gpt-config` outputs a sample YAML template |
| 🔌 **CLI plugins** | Drop Python modules in `~/.lego-gpt/plugins` to add commands |
| ⏲️ **Scheduled cleanup** | Server periodically removes old assets |
| 🧑‍💻 **User management CLI** | `lego-gpt-users` lists and deletes accounts |

&nbsp;

## 3. Quick-Start (Dev)

```bash
# Clone and set up
git clone https://github.com/JGAVEN/Lego-GPT.git
cd Lego-GPT
nvm use # switch to Node 20 if nvm is available

# Optional: copy ``.env.example`` to ``.env`` and adjust settings.
# Front-end builds can also read ``frontend/.env``. Copy ``frontend/.env.example``
# and set ``VITE_API_URL`` if the API runs elsewhere. ``VITE_JWT`` can hold
# a JWT token for commenting and API access.

# Install pnpm (requires Node.js)
npm install -g pnpm@10.5.2

# Install front-end dependencies.
# The script installs from the local pnpm store if possible and fetches from
# the registry when online. Run it once with network access.
# Running it offline before the store is populated prints a brief message and
# skips linting. The script requires `pnpm` to be installed.
./scripts/setup_frontend.sh
# The script also verifies the Cypress binary so UI tests can run offline.

# Install backend dependencies and dev tools (includes `ruff` for linting)
# Add the `[env]` extra to enable `.env` configuration support
python -m pip install --editable ./backend[test,env]
# The dev container's setup script runs this automatically.

# Start Redis (local or Docker)
# docker run -p 6379:6379 -d redis:7
# Optionally set the Redis URL for server and workers
export REDIS_URL=redis://localhost:6379/0
# Moderation queue can be shared via Redis as well
export SUBMISSIONS_REDIS_URL=$REDIS_URL

# Launch the RQ worker in one terminal
# ``--redis-url`` overrides the REDIS_URL env var
# Optional ``--queue`` overrides the QUEUE_NAME env var
export QUEUE_NAME=legogpt
lego-gpt-worker --redis-url "$REDIS_URL" --queue "$QUEUE_NAME" \
  --log-level INFO
# Write worker logs to a file
# lego-gpt-worker --log-file worker.log
# Use a different solver backend with --solver-engine or ORTOOLS_ENGINE
# lego-gpt-worker --solver-engine CBC
# Launch the detector worker in another
lego-detect-worker --redis-url "$REDIS_URL" --queue "$QUEUE_NAME" \
  --model detector/model.pt \
  --log-level INFO
# Log detection worker output
# lego-detect-worker --log-file detect.log
# Append ``--version`` to either worker command to print the version and exit

# Launch the API server in another
export JWT_SECRET=mysecret         # auth secret
export BRICK_INVENTORY=backend/inventory.json  # optional inventory
export DETECTOR_MODEL=detector/model.pt       # optional YOLOv8 weights (or pass --model)
export LEGOGPT_MODEL=/path/to/checkpoint     # optional larger LegoGPT model
# ``--jwt-secret``, ``--redis-url`` and ``--rate-limit`` override the
# corresponding environment variables. Use ``--log-level`` or ``LOG_LEVEL``
# to control verbosity for server and workers.
# Optionally place these variables in a ``.env`` file (see ``.env.example``).
# The backend automatically loads it on startup.
# See ``docs/TOKEN_ROTATION.md`` for rotating the JWT secret.
# See ``docs/SCALABILITY_BENCHMARKING.md`` for load-testing guidance.
# Alternatively set ``LEGOGPT_CONFIG`` or ``--config`` to load settings from a YAML file.
# Generate a starter config with ``lego-gpt-config > config.yaml``.
lego-gpt-server \
  --host 0.0.0.0 \
  --port 8000 \
  --redis-url "$REDIS_URL" \
  --jwt-secret "$JWT_SECRET" \
  --rate-limit 5 \
  --queue "$QUEUE_NAME" \
  --log-level INFO              # http://localhost:8000/health
# Logs can also be written to a file using --log-file or LOG_FILE
#  --log-file server.log
# The `--host` and `--port` options can also be provided via `HOST` and
# `PORT` environment variables. Use `--version` to print the backend version
# and exit.
# Generated assets are written to `backend/static/{uuid}/` by default.
# Pass ``--static-root <dir>`` or set the ``STATIC_ROOT`` environment
# variable to override the directory. ``STATIC_URL_PREFIX`` customises
# the URL prefix returned in API responses (default: ``/static``).
# ``HISTORY_ROOT`` sets the directory used for per-user build history.
# ``EXAMPLE_SOURCES`` is a comma-separated list of instance URLs for federated search.
# Set ``CORS_ORIGINS`` or pass ``--cors-origins <origins>`` to control the
# ``Access-Control-Allow-Origin`` header.
# Set ``S3_BUCKET`` and optional ``S3_URL_PREFIX`` to upload assets to S3/R2.
# Generated files are gzipped before upload when this is enabled.
# Set ``SMTP_HOST`` and ``COMMENT_NOTIFY_EMAIL`` to enable comment notifications.
# Optionally configure ``SMTP_USER``, ``SMTP_PASSWORD`` and ``SMTP_FROM``.

# Start the collaboration server for shared editing
lego-gpt-collab --host 0.0.0.0 --port 8765

# Stream live metrics
lego-gpt-metrics --host 0.0.0.0 --port 8777
# Fetch Prometheus metrics
curl -H "Authorization: Bearer $(cat token.txt)" http://localhost:8000/metrics_prom
# Export metrics history to CSV
lego-gpt-analytics metrics.csv --token $(cat token.txt)
# Push metrics to a data warehouse
lego-gpt-analytics - --token $(cat token.txt) --push-url http://warehouse.example.com/upload

# Access the collaboration demo
Open the PWA and choose **Collaboration Demo** from the main page to try real-time editing. A banner shows how many collaborators are connected.

# Generate a JWT for requests
lego-gpt-token --secret mysecret --sub dev > token.txt

# Check the CLI version
lego-gpt-cli --version
# Enable shell completions
lego-gpt-cli completion bash > /etc/bash_completion.d/lego-gpt

# Test the API via the command-line client
lego-gpt-cli --token $(cat token.txt) generate "a red car"
# Pass a brick inventory JSON file
lego-gpt-cli --token $(cat token.txt) generate "a red car" --inventory my_inv.json
# Download assets to a directory
lego-gpt-cli --token $(cat token.txt) generate "a red car" --out-dir my_build
# Generate multiple models from a file of prompts
lego-gpt-cli --token $(cat token.txt) generate --file prompts.txt
# The CLI loads API_URL and JWT from a .env file if present
# The front-end can be pointed at a custom backend by creating
# `frontend/.env` and setting `VITE_API_URL=http://host:8000`
# Additional commands can be installed by placing Python modules in
# `~/.lego-gpt/plugins` with a `register(subparsers)` function.

# Start the front-end PWA
pnpm --dir frontend run dev    # http://localhost:5173
# The PWA caches generated models in IndexedDB and preview images via a
# service worker so previously viewed results remain available offline.
# Requests made while offline are queued and processed once connectivity returns.
# Browse shared prompts in the Examples page and load them with one click.
# Lint UI code (skips if dependencies are missing)
pnpm --dir frontend run lint
# Lint backend code
ruff check backend detector
# Run UI tests (requires the dev server on another terminal)
pnpm --dir frontend run test:e2e
# Remove assets older than 7 days (preview with --dry-run)
lego-gpt-cleanup --days 7 --dry-run
# Convert an existing .ldr model to glTF
lego-gpt-export model.ldr model.gltf
# Translate example prompts
lego-gpt-translate es --url https://api.example.com/translate
# This command translates example prompts only; the app itself is English-only.
# Set CLEANUP_DAYS and CLEANUP_DRY_RUN in the environment to persist defaults

# Measure API throughput with 4 concurrent requests
python scripts/benchmark_scalability.py --token $(cat token.txt) \
    --requests 20 --concurrency 4
```

### Pre-commit Hooks
`./.codex/setup.sh` installs `pre-commit` and runs `pre-commit install` so
`ruff` checks run automatically on each commit. The configuration lives in
`.pre-commit-config.yaml`.

Run `./scripts/run_tests.sh` to lint and test in one step.
The script runs Cypress UI tests if the dependencies are available.
CI runs the same tests under `coverage` and uploads the report to Codecov.
CI also executes a lightweight scalability benchmark via
`scripts/benchmark_ci.py` to detect performance regressions.

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

This spins up Redis, the API server, a generation worker and the detector worker.

The API will be available at http://localhost:8000/health.
The `/health` endpoint responds with `{ "ok": true, "version": "x.y.z" }` so you
can verify the backend version.

### Production Docker Images

Release tags trigger a workflow that builds CPU and GPU images and publishes
them to GitHub Container Registry.  You can pull the latest versioned images:

```bash
docker pull ghcr.io/<owner>/lego-gpt:v0.5.42        # CPU
docker pull ghcr.io/<owner>/lego-gpt:gpu-v0.5.42    # GPU
```

Run the API server with:

```bash
docker run -p 8000:8000 ghcr.io/<owner>/lego-gpt:v0.5.42
```

Override the command to start a worker or the detector worker as needed.
The Dockerfiles install build tools (`build-essential`, `git` and `libgl1`) so
optional computer‑vision dependencies compile without errors.

### Cloud Deployment

Sample templates are available under [`infra/`](infra/README.md) for deploying
Lego GPT to AWS or Kubernetes. The Terraform configuration sets up AWS App
Runner, while `infra/k8s` contains vanilla Kubernetes manifests. To deploy with
Terraform export the required variables and run `terraform init` followed by
`terraform apply`:

```bash
cd infra/aws
export TF_VAR_api_image=ghcr.io/<owner>/lego-gpt:v0.5.42
export TF_VAR_redis_url=redis://hostname:6379/0
export TF_VAR_jwt_secret=$(openssl rand -hex 32)
terraform init
terraform apply
```

Secrets are provided via environment variables (`TF_VAR_*`) so they are not
committed to version control. Create a `terraform.tfvars` file if you prefer
to keep them on disk. Consider configuring remote state (for example an S3
bucket) so team members share the same Terraform state. The example deploys
the API using AWS App Runner and assumes a Redis instance is already
available. Adjust the `region` variable or other parameters in
[`variables.tf`](infra/aws/variables.tf) to suit your environment.

### Train the Brick Detector

Fine‑tune the YOLOv8 model when you have a labelled dataset. The
`lego-detect-train` console script wraps the `ultralytics` training API:

```bash
lego-detect-train data.yaml --epochs 100 --out detector/model.pt
```

You can also train inside Docker:

```bash
scripts/train_detector.sh /path/to/data.yaml --epochs 100 --out detector/model.pt
```

The resulting weights file can then be referenced via the `DETECTOR_MODEL`
environment variable when running the detector worker. See
[`docs/DETECTOR_DATASET.md`](docs/DETECTOR_DATASET.md) for the required dataset
layout.

#### Render quick-start

Deploy the API and PWA on [Render](https://render.com) using the bundled
`render.yaml` blueprint:

```bash
render blueprint apply render.yaml
```

The configuration spins up a Redis instance, a Python web service running
`uvicorn api:app`, and a static site for the front-end build. Update any
environment variables in the Render dashboard or via `envVarGroups` as needed.

The blueprint defines two API services—`lego-gpt-api-green` and
`lego-gpt-api-blue`. Only the green service is active by default. The blue
service stays disabled until you use it for a blue/green rollout, so it may show
as a failed or pending deploy in the Render dashboard.


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
You can call the endpoint multiple times and merge the returned `brick_counts` objects to build a combined inventory file for one project.

Default rate limit is `5` generate requests per token per minute (configurable via `RATE_LIMIT`).

&nbsp;

## 6. Contributing

1. **One atomic branch per ticket** (`feature/<ticket-slug>`).
2. Follow `docs/PROJECT_BACKLOG.md` for ticket IDs and size.
3. Front-end dependencies are installed via `scripts/setup_frontend.sh`.
   The script attempts an offline install and fetches from the registry if needed.
   Run it once with network access (`pnpm install --dir frontend` works too) so
   future lints and dev builds work offline. The script installs runtime React
   packages plus the linting/dev tools required by `lint_frontend.js`:
   `@eslint/js`, `@types/react`, `@types/react-dom`, `@vitejs/plugin-react`,
   `eslint`, `eslint-config-prettier`, `eslint-plugin-react-hooks`,
   `eslint-plugin-react-refresh`, `globals`, `prettier`, `typescript`,
   `typescript-eslint`, `vite` and `cypress`. Running the setup script offline before the
   store is populated prints a short message explaining the missing packages.
   Run `pnpm --dir frontend run lint` after editing UI code; the command skips if
   dependencies are missing.
   Run `pnpm --dir frontend run test:e2e` to execute Cypress tests when
   the Vite dev server is running.
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

## 8. Project Wrap‑Up & Handoff

All major features are now implemented:

* Upload one or more photos of your bricks. The PWA merges the detections into a single inventory file.
* Generate a construction proposal from that inventory and request alternate builds by changing the prompt or seed.
* Each option is logged under `/history` so you can review past builds.
* When a model is chosen, a PDF with step‑by‑step instructions is available via `instructions_url`.
* The responsive PWA works on laptops and mobile devices with intuitive navigation.

The codebase is ready for rollout. See the Quick‑Start section for running the API, workers and PWA. New maintainers can consult `docs/ARCHITECTURE.md` for component details.

## 9. Maintenance Mode

Lego GPT is feature complete and entering long‑term maintenance. Only security fixes
and community pull requests will be accepted. The repository will be archived
after the final release tag.
See [docs/COMMUNITY_MAINTENANCE.md](docs/COMMUNITY_MAINTENANCE.md) for how to
fork the project and submit security patches. A static
announcement is available at `frontend/public/sunset.html`.
Pinned package versions are listed in
[docs/DEPENDENCY_VERSIONS.md](docs/DEPENDENCY_VERSIONS.md).
See [docs/LTS_POLICY.md](docs/LTS_POLICY.md) for the long-term support window.
Issue triage steps are documented in
[docs/ISSUE_TRIAGE_GUIDE.md](docs/ISSUE_TRIAGE_GUIDE.md).

For creating a new release, follow the steps in [docs/RELEASE_PROCESS.md](docs/RELEASE_PROCESS.md). Documentation is mirrored as a static site (see [docs/ARCHIVE_SITE.md](docs/ARCHIVE_SITE.md)).
