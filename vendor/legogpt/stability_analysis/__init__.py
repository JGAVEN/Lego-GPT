"""Lightweight wrappers for stability and connectivity analysis."""

from dataclasses import dataclass


@dataclass
class StabilityConfig:
    world_dimension: tuple[int, int, int] = (20, 20, 20)


def stability_score(*_args, **_kwargs):
    """Placeholder; original solver has been removed."""
    raise NotImplementedError("Stability solver not bundled")


from .connectivity_analysis import connectivity_score

__all__ = ["StabilityConfig", "stability_score", "connectivity_score"]
