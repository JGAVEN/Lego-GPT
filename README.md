# Lego GPT

Generate buildable LEGO® creations directly from your phone’s browser.

Lego GPT pairs the CMU **LegoGPT** Llama‑3 1B model with a thin FastAPI inference
gateway and a React / Three.js Progressive‑Web‑App front‑end.  
The model converts natural‑language prompts into **LDraw** brick assemblies,
renders a PNG preview, and serves the `.ldr` file for 3‑D manipulation or real‑life
building.

## Repository layout

```
.
├── backend/          # FastAPI app + model wrapper
├── frontend/         # React (Vite) PWA with Three.js viewer
├── src/legogpt/      # LegoGPT git‑submodule (read‑only)
├── docs/             # Project documentation
└── Dockerfile*       # Dev & production images
```

See **docs/ARCHITECTURE.md** for full details.

## Quick‑start (local dev)

```bash
# clone + init submodule
git clone git@github.com:JGAVEN/Lego-GPT.git
cd Lego-GPT && git submodule update --init

# backend
cd backend
poetry install
export HF_TOKEN=<your-huggingface-token>
poetry run uvicorn api:app --reload   # http://localhost:8000/health

# frontend (in another terminal)
cd ../frontend
pnpm install
pnpm dev  # http://localhost:5173
```

## License

MIT. LEGO® is a trademark of the LEGO Group of companies which does not sponsor,
authorize or endorse this project.
