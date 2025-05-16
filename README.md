# Lego GPT

Generate buildable LEGO® creations right from your browser.

| Component            | Status   | Notes                                                       |
|----------------------|----------|-------------------------------------------------------------|
| Backend `/health`    | ✅ Done  | FastAPI + Poetry                                            |
| Backend `/generate`  | ✅ Mock  | Returns PNG/LDR/brick_counts with mocked LegoGPT wrapper    |
| Integration Tests    | ✅ Done  | `backend/tests/test_generate.py` passes with mock model     |
| Docker Dev Stack     | ✅ Done  | `docker compose up` runs backend                            |
| Front‑end Scaffold   | ✅ Done  | React + Vite + TypeScript shows “Hello LegoGPT”             |
| CI Stub              | ✅ Done  | GitHub Action prints “CI alive”                             |
| 3‑D Viewer           | ⬜ TODO  | Three.js LDrawLoader (Ticket 2.2)                           |
| Auth & Rate‑limit    | ⬜ TODO  | Planned after core flow is solid                            |

---

## Local Quick‑Start

```bash
git clone git@github.com:JGAVEN/Lego-GPT.git
cd Lego-GPT
git submodule update --init                        # pulls CMU LegoGPT code

# ─── Backend ───
cd backend
poetry install --no-root                           # installs FastAPI, Torch, etc.
poetry run uvicorn api:app --reload                # http://localhost:8000/health

# ─── Front‑end ───
cd ../frontend
pnpm install
pnpm dev                                           # http://localhost:5173
```

---

## Docker Dev Stack

```bash
docker compose up --build                          # builds & runs backend
curl -X POST http://localhost:8000/generate \
     -H "Content-Type: application/json" \
     -d '{"text":"blue cube","seed":42}'
```

---

## Project Structure

```
.
├── backend/                 # FastAPI app, Poetry project
│   ├── api.py               # routes (/health, /generate)
│   ├── inference.py         # LegoGPT wrapper (mock)
│   ├── tests/               # pytest suite
│   └── static/              # generated PNG / LDR files (ignored)
├── docs/                    # architecture & guidance
├── frontend/                # React + Vite app
├── src/legogpt/             # CMU LegoGPT as git-submodule
└── docker-compose.yml       # dev stack
```

See **docs/ARCHITECTURE.md** for detailed diagrams and flow.

---

## Contributing

* Follow the *one‑step‑at‑a‑time GPT‑4o* workflow in **docs/CONTRIBUTING.md**.  
* After each merged ticket, update docs and **CHANGELOG.md**.  
* Keep generated artefacts out of git (`backend/static/` is ignored).
