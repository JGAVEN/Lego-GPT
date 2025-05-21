"""
Lightweight stub that satisfies `from legogpt.models.llm import LLM`
without downloading a real HuggingFace model.
"""
class LLM:
    def __init__(self, *_, **__):
        pass
    def __call__(self, prompt: str):
        # Return a trivial response so downstream code keeps running
        return "brick brick brick"
