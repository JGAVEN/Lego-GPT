"""
Unified interface for any LEGO stability MIP backend.

Add concrete back-ends (e.g. `ortools_solver.py`, `gurobi_solver.py`)
that implement `ILPSolver.solve(bricks) -> bricks`.
"""
from __future__ import annotations

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Protocol, runtime_checkable

# ------------------------------------------------------------------
# Ensure the vendored LegoGPT library is importable.
# Repo layout: repo_root/vendor/legogpt/…
# We insert the vendor directory so `import legogpt` works
# from anywhere (tests, backend, worker containers, etc.).
# ------------------------------------------------------------------
vendor_root = Path(__file__).resolve().parents[2] / "vendor"
if vendor_root.exists() and str(vendor_root) not in sys.path:
    sys.path.insert(0, str(vendor_root))
# ------------------------------------------------------------------

# Re-use Brick dataclass from the CMU sub-module
from legogpt.data import LegoBrick  # noqa: E402


@runtime_checkable
class SupportsStability(Protocol):
    """Minimal protocol for a LEGO structure object we can stabilise."""
    bricks: List[LegoBrick]


class ILPSolver(ABC):
    """Abstract base class for physics-stability solvers."""

    @abstractmethod
    def solve(self, structure: SupportsStability) -> SupportsStability:  # pragma: no cover
        """
        Return a *stable* clone of the input structure or raise an
        `UnstableError` if no feasible subset exists.
        """
        raise NotImplementedError
