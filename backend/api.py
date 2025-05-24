"""Minimal API functions for offline use."""
from pathlib import Path
from backend.inference import generate
from backend import __version__, STATIC_ROOT, STATIC_URL_PREFIX


def health() -> dict:
    """Return service liveness and version information."""
    return {"ok": True, "version": __version__}


def generate_lego_model(
    prompt: str, seed: int = 42, inventory_filter: dict[str, int] | None = None
) -> dict:
    """Run the model and return URLs for the generated preview and models."""
    png_path, ldr_path, gltf_path, brick_counts = generate(
        prompt, seed, inventory_filter
    )
    rel_png = Path(png_path).resolve().relative_to(STATIC_ROOT.parent)
    png_url = f"{STATIC_URL_PREFIX}/{rel_png.parent.name}/preview.png"
    ldr_url = None
    gltf_url = None
    if ldr_path:
        rel_ldr = Path(ldr_path).resolve().relative_to(STATIC_ROOT.parent)
        ldr_url = f"{STATIC_URL_PREFIX}/{rel_ldr.parent.name}/model.ldr"
    if gltf_path:
        rel_gltf = Path(gltf_path).resolve().relative_to(STATIC_ROOT.parent)
        gltf_url = f"{STATIC_URL_PREFIX}/{rel_gltf.parent.name}/model.gltf"
    return {
        "png_url": png_url,
        "ldr_url": ldr_url,
        "gltf_url": gltf_url,
        "brick_counts": brick_counts,
    }
