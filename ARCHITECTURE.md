# Architecture

```
┌──────────────┐   HTTPS POST /generate   ┌────────────────────────────┐
│  PWA Client  │◄────────────────────────►│  FastAPI Gateway (API)     │
│  React +     │                          │  • JWT auth (future)       │
│  Three.js    │ PNG preview + .ldr file  │  • Task queue (Redis)      │
└────▲─────────┘                          │  • Model worker (CUDA)     │
     │                                    └──────────▲────────────────┘
     │                                                   │
     │  .ldr parsed & viewed                             │
     ▼                                                   │
Three.js LDrawViewer                        LegoGPT model (Llama‑3 1B)
```

| Layer | Responsibility | Tech |
|-------|----------------|------|
|Front‑end | Prompt form, preview image, 3‑D viewer, PWA shell | React 18, Vite, Three.js (`LDrawLoader`) |
|API | Auth, rate‑limit, task enqueue, static file links | FastAPI, Pydantic, Celery (alt. RQ) |
|Worker | Lazy‑load model, run `generate()`, save PNG + LDR | Python 3.10, CUDA 12.2, HuggingFace `transformers` |
|Storage | Serve artifacts, keep 7‑day TTL | Local `/static`, S3 in prod |

## Data flow

1. **/generate** – client POSTs `{text, seed}`.  
2. Gateway pushes job to queue, streams job‑id.  
3. Worker loads LegoGPT, produces PNG + `.ldr`, uploads to `/static`.  
4. Gateway returns `{png_url, ldr_url, brick_counts}`.  
5. Client shows PNG immediately, lazy‑loads LDR into Three.js viewer.

## Scaling notes

* Start with a single GPU container (A10G 24 GB) – <2 s/token, 3 requests/s.  
* Upgrade to queue + N workers once concurrency >5.  
* Serve static from CloudFront or Cloudflare R2 for global latency.  
* Future: quantize model (INT4) for CPU‑only fallback.

