import os
import uuid
from pathlib import Path

MODEL = None

def load_model():
    global MODEL
    if MODEL is None:
        from legogpt.models.legogpt import LegoGPT, LegoGPTConfig
        config = LegoGPTConfig()  # Customize here if needed
        MODEL = LegoGPT(config)
    return MODEL

def generate(prompt: str, seed: int):
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
