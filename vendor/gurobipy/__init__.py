"""
Stub for gurobipy so LegoGPT can import it without requiring Gurobi.
Only the minimal symbols LegoGPT touches are defined.
"""
class Model: ...
def quicksum(*args, **kwargs): return sum(args)
def LinExpr(*args, **kwargs): return 0
class GRB: pass
