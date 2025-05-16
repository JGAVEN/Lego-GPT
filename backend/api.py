from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from backend.inference import generate


router = APIRouter()

@router.post("/generate")
async def generate_lego_model(
    prompt: str = Body(...), seed: int = Body(42)
):
    png_path, ldr_path, brick_counts = generate(prompt, seed)

    static_prefix = png_path.split("static/")[-1].rsplit("/", 1)[0]
    return JSONResponse({
        "png_url": f"/static/{static_prefix}/preview.png",
        "ldr_url": f"/static/{static_prefix}/model.ldr",
        "brick_counts": brick_counts
    })

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(router)

app.mount("/static", StaticFiles(directory="backend/static"), name="static")
