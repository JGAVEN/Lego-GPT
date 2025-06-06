from __future__ import annotations
from pathlib import Path
from backend.inference import generate
from backend import STATIC_ROOT, STATIC_URL_PREFIX
from backend.storage import maybe_upload_assets


def generate_lego_model(
    prompt: str, seed: int = 42, inventory_filter: dict[str, int] | None = None
) -> dict:
    """Run the model and return URLs for the generated preview and models."""
    png_path, ldr_path, gltf_path, pdf_path, brick_counts = generate(
        prompt, seed, inventory_filter
    )

    paths = [Path(png_path)]
    if ldr_path:
        paths.append(Path(ldr_path))
    if gltf_path:
        paths.append(Path(gltf_path))
    if pdf_path:
        paths.append(Path(pdf_path))

    urls, uploaded = maybe_upload_assets(paths)
    pdf_url = None
    if uploaded:
        url_iter = iter(urls)
        png_url = next(url_iter)
        ldr_url = next(url_iter) if ldr_path else None
        gltf_url = next(url_iter) if gltf_path else None
        pdf_url = next(url_iter) if pdf_path else None
    else:
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
        if pdf_path:
            rel_pdf = Path(pdf_path).resolve().relative_to(STATIC_ROOT.parent)
            pdf_url = f"{STATIC_URL_PREFIX}/{rel_pdf.parent.name}/instructions.pdf"

    return {
        "png_url": png_url,
        "ldr_url": ldr_url,
        "gltf_url": gltf_url,
        "brick_counts": brick_counts,
        "instructions_url": pdf_url,
    }
