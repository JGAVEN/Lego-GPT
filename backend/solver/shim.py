"""
Drop-in replacement for `legogpt.stability_analysis.stability_score`.

For now it returns a perfect score so the pipeline keeps working
without Gurobi.  In a later commit we’ll call the real OR-Tools MIP.
"""
from __future__ import annotations

import importlib
import sys
from typing import Any, Tuple

from legogpt.data import LegoStructure  # type: ignore
from backend.solver import get_solver

_solver = get_solver()  # OrtoolsSolver


def stability_score(
    lego_structure: str | dict,
    lego_library: Any,
    cfg: Any = None,
) -> Tuple[float, None, None, None, None]:
    # Convert JSON → object if needed
    if isinstance(lego_structure, (str, bytes)):
        structure = LegoStructure.from_json(lego_structure)
    else:
        structure = LegoStructure.from_dict(lego_structure)

    # TODO: use _solver.solve(structure) and compute real score
    return 1.0, None, None, None, None


# ---- expose on the original import path ---------------------------------
module_path = "legogpt.stability_analysis"
module = importlib.import_module(module_path)
module.stability_score = stability_score  # type: ignore[attr-defined]
sys.modules[f"{module_path}.stability_score"] = stability_score
# -------------------------------------------------------------------------
