"""
Backend façade that wraps the LegoGPT model and handles disk output.

`backend.solver.shim` is imported *solely* for its side-effect:
it monkey-patches `legogpt.stability_analysis.stability_score`
so the pipeline uses our open-source ILP backend.
"""
from __future__ import annotations

import uuid
from pathlib import Path

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

        config = LegoGPTConfig()  # customise here if needed
        MODEL = LegoGPT(config)
    return MODEL


# --------------------------------------------------------------------------- #
#                               Entry point                                   #
# --------------------------------------------------------------------------- #
def generate(prompt: str, seed: int | None = None):
    """
    Generate a new LEGO structure preview.

    Parameters
    ----------
    prompt : str
        Natural-language prompt from the user.
    seed : int | None
        Optional RNG seed for reproducibility.

    Returns
    -------
    tuple[str, str | None, dict]
        PNG path, optional LDraw path, and brick-count dict.
    """
    model = load_model()
    result = model.generate(prompt, seed=seed)

    run_id = str(uuid.uuid4())
    output_dir = Path("backend/static") / run_id
    output_dir.mkdir(parents=True, exist_ok=True)

    png_path = output_dir / "preview.png"
    ldr_path = output_dir / "model.ldr"

    # Always save PNG
    png_path.write_bytes(result["png"])

    # Save .ldr only if present
    if result.get("ldr"):
        ldr_path.write_text(result["ldr"])
        ldr_path_str: str | None = str(ldr_path)
    else:
        ldr_path_str = None

    return str(png_path), ldr_path_str, result["brick_counts"]
