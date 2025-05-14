# Lego GPT

Generate buildable LEGO® creations right from your phone.

## Why?

**Lego GPT** wraps the CMU LegoGPT model (Llama‑3 1B, fine‑tuned to output LDraw brick assemblies) behind a FastAPI backend and a React (Three.js) front‑end. It lets you:

* type or dictate a prompt (“red dragon with golden wings”),
* receive a PNG preview in seconds,
* orbit a full 3‑D model in your browser,
* download the `.ldr` to build it in real life.

## High‑level architecture

```
┌──────────────┐   https POST /generate    ┌───────────────────────┐
│  Phone (PWA) │◄──────────────────────────►│  FastAPI gateway      │
│  React +     │                           │  • token auth         │
│  Three.js    │     S3 / static URLs      │  • queue + GPU worker │
└────▲─────────┘                           └──────────▲────────────┘
     │  .ldr/.png (lazy‑load)                          │
     │                                                 │
     ▼                                                 │
        Three.js LDrawViewer               LegoGPT inference (CUDA)
```

## Quick‑start (local dev)

```bash
# 1. clone repo and submodule
git clone git@github.com:JGAVEN/lego-gpt.git
cd lego-gpt
git submodule update --init

# 2. backend (Python 3.10)
cd backend
poetry install
export HF_TOKEN=<your-huggingface-token>
poetry run uvicorn api:app --reload  # http://localhost:8000/health

# 3. front‑end (Node 20)
cd ../frontend
pnpm install
pnpm dev  # http://localhost:5173
```
