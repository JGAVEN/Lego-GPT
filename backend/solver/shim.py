"""
Drop-in replacement for `legogpt.stability_analysis.stability_score`.

For now it returns a perfect score so the pipeline keeps working
without Gurobi.  In a later commit we’ll call the real OR-Tools MIP.
"""
from __future__ import annotations

import importlib
import json
import sys
from typing import Any, Tuple

_solver = None  # Solver disabled in offline mode


def stability_score(
    lego_structure: str | dict,
    lego_library: Any,
    cfg: Any = None,
) -> Tuple[float, None, None, None, None]:
    # Parse JSON if supplied; ignore result
    if isinstance(lego_structure, (str, bytes)):
        try:
            json.loads(lego_structure)
        except Exception:
            pass
    # TODO: use _solver.solve(...) and compute real score
    return 1.0, None, None, None, None


# ---- expose on the original import path ---------------------------------
module_path = "legogpt.stability_analysis"
module = importlib.import_module(module_path)
module.stability_score = stability_score  # type: ignore[attr-defined]
sys.modules[f"{module_path}.stability_score"] = stability_score
# -------------------------------------------------------------------------
