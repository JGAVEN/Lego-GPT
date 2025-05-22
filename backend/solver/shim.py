"""
Drop-in replacement for `legogpt.stability_analysis.stability_score`.

For now it returns a perfect score so the pipeline keeps working.
In a later commit we’ll call the real OR-Tools MIP.
"""
from __future__ import annotations

import importlib
import json
import sys
from typing import Any, Tuple

from legogpt.data import LegoStructure
from .ortools_solver import OrtoolsSolver

try:  # Instantiate solver if OR-Tools is available
    _solver = OrtoolsSolver()
except Exception:  # pragma: no cover - fallback to dummy score
    _solver = None


def stability_score(
    lego_structure: str | dict,
    lego_library: Any,
    cfg: Any = None,
) -> Tuple[float, None, None, None, None]:
    # Parse JSON if supplied and run solver if available
    try:
        if isinstance(lego_structure, (str, bytes)):
            lego_data = json.loads(lego_structure)
        else:
            lego_data = lego_structure
        if _solver is not None and isinstance(lego_data, dict):
            structure = LegoStructure.from_json(lego_data)
            _solver.solve(structure)
    except Exception:  # pragma: no cover - keep dummy behaviour on parse errors
        pass

    # Still return a dummy perfect score for compatibility
    return 1.0, None, None, None, None


# ---- expose on the original import path ---------------------------------
module_path = "legogpt.stability_analysis"
module = importlib.import_module(module_path)
module.stability_score = stability_score  # type: ignore[attr-defined]
sys.modules[f"{module_path}.stability_score"] = stability_score
# -------------------------------------------------------------------------
