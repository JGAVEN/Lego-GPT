"""
Ultra-light stub of the CMU LegoGPT model so the backend runs without
heavy dependencies.  Implements all symbols that models/__init__.py imports.
"""

from base64 import b64decode


# --------------------------------------------------------------------------- #
# Minimal config & dummy LLM
# --------------------------------------------------------------------------- #
class LegoGPTConfig:
    """Placeholder for the real config class."""
    pass


class LLM:
    """Tiny no-op language model stub."""

    def __init__(self, *_, **__):
        pass

    def __call__(self, prompt: str) -> str:
        return "brick brick brick"


# --------------------------------------------------------------------------- #
# Main stub model
# --------------------------------------------------------------------------- #
class LegoGPT:
    """Stubbed LegoGPT model with a minimal generate() implementation."""

    def __init__(self, *_, **__):
        self.cfg = LegoGPTConfig()
        self.llm = LLM()

    # FastAPI’s backend/inference.py calls this
    def generate(self, prompt: str, seed: int | None = None):
        """Return a 1×1 transparent PNG plus empty brick stats."""
        png_b64 = (
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGMA"
            "AQAABQABDQottAAAAABJRU5ErkJggg=="
        )
        png_bytes = b64decode(png_b64)

        return {
            "png": png_bytes,        # raw bytes for backend/inference.py
            "png_b64": png_b64,      # convenient for frontend preview
            "ldr": None,
            "brick_counts": {},
        }


# --------------------------------------------------------------------------- #
# Helper functions that models/__init__.py re-exports
# --------------------------------------------------------------------------- #
def create_instruction(*_, **__) -> str:
    return "instruction"


def create_instruction_zero_shot(*_, **__) -> str:
    return "zero-shot instruction"


def create_instruction_few_shot(*_, **__) -> str:
    return "few-shot instruction"
