"""
Backend façade that wraps the LegoGPT model and handles disk output.

`backend.solver.shim` is imported *solely* for its side-effect:
it monkey-patches `legogpt.stability_analysis.stability_score`
so the pipeline uses our open-source ILP backend.
"""
from __future__ import annotations

import uuid
import os
from backend import STATIC_ROOT

from backend.export import ldr_to_gltf
from backend.inventory import filter_counts

import backend.solver.shim  # noqa: F401  (forces monkey-patch)

MODEL = None


# --------------------------------------------------------------------------- #
#                              Model loading                                  #
# --------------------------------------------------------------------------- #
def load_model():
    """Lazily construct and cache the LegoGPT model (or stub)."""
    global MODEL
    if MODEL is None:
        from legogpt.models.legogpt import LegoGPT, LegoGPTConfig
        model_path = os.getenv("LEGOGPT_MODEL")
        if model_path and hasattr(LegoGPT, "from_pretrained"):
            MODEL = LegoGPT.from_pretrained(model_path)
        else:
            config = LegoGPTConfig()  # customise here if needed
            MODEL = LegoGPT(config)
    return MODEL


# --------------------------------------------------------------------------- #
#                               Entry point                                   #
# --------------------------------------------------------------------------- #
def generate(prompt: str, seed: int | None = None, inventory_filter: dict[str, int] | None = None):
    """
    Generate a new LEGO structure preview.

    Parameters
    ----------
    prompt : str
        Natural-language prompt from the user.
    seed : int | None
        Optional RNG seed for reproducibility.
    inventory_filter : dict[str, int] | None
        Optional inventory map to limit brick counts.

    Returns
    -------
    tuple[str, str | None, str | None, dict]
        PNG path, optional LDraw and glTF paths, and brick-count dict.
    """
    model = load_model()
    result = model.generate(prompt, seed=seed)

    run_id = str(uuid.uuid4())
    output_dir = STATIC_ROOT / run_id
    output_dir.mkdir(parents=True, exist_ok=True)

    png_path = output_dir / "preview.png"
    ldr_path = output_dir / "model.ldr"
    gltf_path = output_dir / "model.gltf"

    # Always save PNG
    png_path.write_bytes(result["png"])

    # Save .ldr only if present
    if result.get("ldr"):
        ldr_path.write_text(result["ldr"])
        ldr_path_str: str | None = str(ldr_path)
        ldr_to_gltf(ldr_path, gltf_path)
        gltf_path_str: str | None = str(gltf_path)
    else:
        ldr_path_str = None
        gltf_path_str = None

    counts = result.get("brick_counts", {})
    counts = filter_counts(counts, inventory_filter)
    return str(png_path), ldr_path_str, gltf_path_str, counts
