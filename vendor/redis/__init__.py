"""Minimal redis stub for offline tests."""

class Redis:
    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def from_url(cls, url: str):
        return cls()
