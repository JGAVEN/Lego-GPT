"""Solver auto-loader.

Call `get_solver()` to obtain the first available ILP backend.
Usage:
    from backend.solver import get_solver
    solver = get_solver()          # returns an ILPSolver instance
    stable = solver.solve(...)

The loader preference order is:
1. OrtoolsSolver (HiGHS / CBC – MIT)
2. GurobiSolver   (commercial, optional – not yet implemented here)

If no backend is available, `RuntimeError` is raised.
"""
from importlib import import_module
from typing import Type

from .base import ILPSolver

_CANDIDATES: list[tuple[str, str]] = [
    ("backend.solver.ortools_solver", "OrtoolsSolver"),
    # ("backend.solver.gurobi_solver", "GurobiSolver"),  # future
]


def _try_import(path: str, cls_name: str) -> Type[ILPSolver] | None:
    try:
        mod = import_module(path)
        cls = getattr(mod, cls_name)
        if issubclass(cls, ILPSolver):
            return cls
    except Exception:  # pragma: no cover
        return None
    return None


def get_solver() -> ILPSolver:
    """Return the first backend that imports & initialises cleanly."""
    for module_path, cls_name in _CANDIDATES:
        cls = _try_import(module_path, cls_name)
        if cls is not None:
            return cls()
    raise RuntimeError("No ILP solver backend available")
