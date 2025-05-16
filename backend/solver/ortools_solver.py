"""
HiGHS / CBC implementation of ILPSolver.

Initial stub: simply returns the input unchanged so the import path works.
We'll replace `.solve()` with full stability constraints in the next steps.
"""
from __future__ import annotations
from typing import cast

from ortools.linear_solver import pywraplp

from .base import ILPSolver, SupportsStability


class OrtoolsSolver(ILPSolver):
    def __init__(self, backend: str = "HIGHs"):
        # Keep a reference for future model builds
        self.backend = backend
        # Quick self-test: create a dummy solver instance
        self._probe = pywraplp.Solver.CreateSolver(backend)
        if self._probe is None:
            raise RuntimeError(f"OR-Tools backend '{backend}' unavailable")

    def solve(self, structure: SupportsStability) -> SupportsStability:  # noqa: D401
        """
        (Stub) Return the structure untouched.

        Full MIP model will be added in a later commit.
        """
        return cast(SupportsStability, structure)
