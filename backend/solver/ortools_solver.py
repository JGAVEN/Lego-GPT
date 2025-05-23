"""OR-Tools implementation of :class:`ILPSolver`.

The solver keeps a stable subset of bricks using a small MIP model.
If OR-Tools is unavailable (e.g. offline tests), a simple Python
fallback performs the same checks.
"""
from __future__ import annotations
from typing import List, cast

try:  # OR-Tools might not be available in minimal CI images
    from ortools.linear_solver import pywraplp
    _ORTOOLS_AVAILABLE = True
except Exception:  # pragma: no cover - fallback for offline tests
    pywraplp = None  # type: ignore
    _ORTOOLS_AVAILABLE = False

from .base import ILPSolver, SupportsStability
from legogpt.data import LegoBrick


class _Structure:
    """Minimal structure returned by the solver."""

    def __init__(self, bricks: List[LegoBrick], world_dim: int = 20) -> None:
        self.bricks = list(bricks)
        self.world_dim = world_dim


class OrtoolsSolver(ILPSolver):
    def __init__(self, backend: str = "HIGHs"):
        # Keep a reference for future model builds
        self.backend = backend
        if _ORTOOLS_AVAILABLE:
            # Quick self-test: create a dummy solver instance
            self._probe = pywraplp.Solver.CreateSolver(backend)
            if self._probe is None:
                raise RuntimeError(f"OR-Tools backend '{backend}' unavailable")
        else:  # pragma: no cover - used only in offline test envs
            self._probe = None

    def _overlap(self, a: LegoBrick, b: LegoBrick) -> bool:
        """Return True if two bricks overlap in the x/y plane."""
        return not (
            a.x + a.h <= b.x or b.x + b.h <= a.x or a.y + a.w <= b.y or b.y + b.w <= a.y
        )

    def _connected(self, a: LegoBrick, b: LegoBrick) -> bool:
        """Return True if ``b`` sits directly on top of ``a``."""
        if a.z > b.z:
            a, b = b, a
        return a.z == b.z - 1 and self._overlap(a, b)

    def _filter_connected(self, bricks: List[LegoBrick]) -> List[LegoBrick]:
        """Return bricks connected to the ground via stack connections."""
        graph: list[list[int]] = [[] for _ in bricks]
        ground = []
        for i, bi in enumerate(bricks):
            if bi.z == 0:
                ground.append(i)
        for i, bi in enumerate(bricks):
            for j in range(i + 1, len(bricks)):
                bj = bricks[j]
                if self._connected(bi, bj):
                    graph[i].append(j)
                    graph[j].append(i)
        visited = set(ground)
        stack = list(ground)
        while stack:
            idx = stack.pop()
            for j in graph[idx]:
                if j not in visited:
                    visited.add(j)
                    stack.append(j)
        return [b for i, b in enumerate(bricks) if i in visited]

    def solve(self, structure: SupportsStability) -> SupportsStability:  # noqa: D401
        """Return a stable subset of ``structure`` using a small MIP model."""

        bricks: List[LegoBrick] = list(structure.bricks)

        if not _ORTOOLS_AVAILABLE:
            kept: List[LegoBrick] = []
            for b in bricks:
                if b.z > 0:
                    valid = True
                    for x in range(b.x, b.x + b.h):
                        for y in range(b.y, b.y + b.w):
                            supported = False
                            for sb in kept:
                                if sb.z == b.z - 1 and sb.x <= x < sb.x + sb.h and sb.y <= y < sb.y + sb.w:
                                    supported = True
                                    break
                            if not supported:
                                valid = False
                                break
                        if not valid:
                            break
                    if not valid:
                        continue
                kept.append(b)
            kept = self._filter_connected(kept)
            world_dim = getattr(structure, "world_dim", 20)
            return cast(SupportsStability, _Structure(kept, world_dim=world_dim))

        solver = pywraplp.Solver.CreateSolver(self.backend)
        if solver is None:  # pragma: no cover - checked in __init__
            raise RuntimeError("Failed to create OR-Tools solver instance")

        keep_vars = [solver.BoolVar(f"keep_{i}") for i in range(len(bricks))]

        # Objective: keep as many bricks as possible
        solver.Maximize(solver.Sum(keep_vars))

        # Stability constraints
        for i, bi in enumerate(bricks):
            if bi.z == 0:
                continue
            for x in range(bi.x, bi.x + bi.h):
                for y in range(bi.y, bi.y + bi.w):
                    supporters = []
                    for j, bj in enumerate(bricks):
                        if bj.z == bi.z - 1 and bj.x <= x < bj.x + bj.h and bj.y <= y < bj.y + bj.w:
                            supporters.append(keep_vars[j])
                    if supporters:
                        solver.Add(solver.Sum(supporters) >= keep_vars[i])
                    else:
                        solver.Add(keep_vars[i] == 0)

        status = solver.Solve()
        if status != pywraplp.Solver.OPTIMAL:  # pragma: no cover
            kept = bricks
        else:
            kept = [b for b, var in zip(bricks, keep_vars) if var.solution_value() > 0.5]
        kept = self._filter_connected(kept)
        world_dim = getattr(structure, "world_dim", 20)
        return cast(SupportsStability, _Structure(kept, world_dim=world_dim))
