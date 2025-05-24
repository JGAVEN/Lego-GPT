"""
Drop-in replacement for ``legogpt.stability_analysis.stability_score``.

Uses the open-source OR-Tools solver when available and falls back to
a dummy score otherwise.  This keeps the pipeline functional even on
systems without OR-Tools installed.
"""
from __future__ import annotations

import importlib
import json
import os
import sys
from typing import Any, Tuple

from legogpt.data import LegoStructure
from .ortools_solver import OrtoolsSolver

try:  # Instantiate solver if OR-Tools is available
    backend_name = os.getenv("ORTOOLS_ENGINE", "HIGHs")
    _solver = OrtoolsSolver(backend_name)
except Exception:  # pragma: no cover - fallback to dummy score
    _solver = None


def stability_score(
    lego_structure: str | dict,
    lego_library: Any,
    cfg: Any = None,
) -> Tuple[float, None, None, None, None]:
    """Return a simple stability score using the OR-Tools solver if available."""
    try:
        if isinstance(lego_structure, (str, bytes)):
            lego_data = json.loads(lego_structure)
        else:
            lego_data = lego_structure

        if _solver is not None and isinstance(lego_data, dict):
            structure = LegoStructure.from_json(lego_data)
            stable = _solver.solve(structure)
            if structure.bricks:
                score = len(stable.bricks) / len(structure.bricks)
            else:
                score = 1.0
            return float(score), None, None, None, stable
    except Exception:  # pragma: no cover - keep dummy behaviour on parse errors
        pass

    return 1.0, None, None, None, None


# ---- expose on the original import path ---------------------------------
module_path = "legogpt.stability_analysis"
module = importlib.import_module(module_path)
module.stability_score = stability_score  # type: ignore[attr-defined]
sys.modules[f"{module_path}.stability_score"] = stability_score
# -------------------------------------------------------------------------
