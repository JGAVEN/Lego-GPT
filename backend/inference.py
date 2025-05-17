"""
Backend façade that wraps the LegoGPT model and handles disk output.

`backend.solver.shim` is imported *solely* for its side-effect:
it monkey-patches `legogpt.stability_analysis.stability_score`
so the pipeline uses our open-source ILP backend instead of Gurobi.
"""
from __future__ import annotations

import os
import uuid
from pathlib import Path

import backend.solver.shim  # noqa: F401  (forces monkey-patch)

MODEL = None


def load_model():
    """Lazily construct and cache the LegoGPT model."""
    global MODEL
    if MODEL is None:
        from legogpt.models.legogpt import LegoGPT, LegoGPTConfig

        config = LegoGPTConfig()  # customise here if needed
        MODEL = LegoGPT(config)
    return MODEL


def generate(prompt: str, seed: int):
    """
    Generate a new LEGO structure preview.

    Returns
    -------
    tuple[str, str, dict]
        PNG path, LDraw path, and brick-count dict.
    """
    model = load_model()
    result = model.generate(prompt, seed=seed)

    run_id = str(uuid.uuid4())
    output_dir = Path("backend/static") / run_id
    output_dir.mkdir(parents=True, exist_ok=True)

    png_path = output_dir / "preview.png"
    ldr_path = output_dir / "model.ldr"

    with open(png_path, "wb") as f:
        f.write(result["png"])
    with open(ldr_path, "w") as f:
        f.write(result["ldr"])

    return str(png_path), str(ldr_path), result["brick_counts"]
