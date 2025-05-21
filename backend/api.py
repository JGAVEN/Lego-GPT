"""Minimal API functions for offline use."""
from pathlib import Path
from backend.inference import generate

STATIC_ROOT = Path(__file__).parent / "static"


def health() -> dict:
    return {"ok": True}


def generate_lego_model(prompt: str, seed: int = 42) -> dict:
    png_path, ldr_path, brick_counts = generate(prompt, seed)
    rel_png = Path(png_path).resolve().relative_to(STATIC_ROOT.parent)
    png_url = f"/static/{rel_png.parent.name}/preview.png"
    ldr_url = None
    if ldr_path:
        rel_ldr = Path(ldr_path).resolve().relative_to(STATIC_ROOT.parent)
        ldr_url = f"/static/{rel_ldr.parent.name}/model.ldr"
    return {"png_url": png_url, "ldr_url": ldr_url, "brick_counts": brick_counts}
