"""
Unified interface for any LEGO stability MIP backend.

Add concrete back-ends (e.g. `ortools_solver.py`, `gurobi_solver.py`)
that implement `ILPSolver.solve(bricks) -> bricks`.
"""
from __future__ import annotations

# ------------------------------------------------------------------
# Ensure the CMU LegoGPT sub-module is importable
# Repo layout: repo_root/src/legogpt/src/legogpt/…
# We insert the inner "src" dir into sys.path so `import legogpt` works
# from anywhere (tests, backend, worker containers, etc.).
# ------------------------------------------------------------------
import sys
from pathlib import Path

submodule_root = Path(__file__).resolve().parents[2] / "src" / "legogpt" / "src"
if submodule_root.exists() and str(submodule_root) not in sys.path:
    sys.path.insert(0, str(submodule_root))
# ------------------------------------------------------------------

from abc import ABC, abstractmethod
from typing import List, Protocol, runtime_checkable

# Re-use Brick dataclass from the CMU sub-module
from legogpt.data import LegoBrick


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
