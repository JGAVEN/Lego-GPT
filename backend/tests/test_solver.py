import sys
import unittest
from pathlib import Path

# Ensure vendor modules are importable
project_root = Path(__file__).resolve().parents[2]
vendor_root = project_root / "vendor"
for p in (project_root, vendor_root):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from dataclasses import dataclass

from backend.solver import get_solver  # noqa: E402
from legogpt.data import LegoBrick  # noqa: E402


@dataclass
class SimpleStructure:
    bricks: list[LegoBrick]
    world_dim: int = 20


class SolverBehaviourTests(unittest.TestCase):
    def setUp(self):
        self.solver = get_solver()

    def test_single_ground_brick(self):
        structure = SimpleStructure([LegoBrick(h=1, w=1, x=0, y=0, z=0)])
        result = self.solver.solve(structure)
        self.assertEqual(len(result.bricks), 1)

    def test_floating_brick_removed(self):
        structure = SimpleStructure([LegoBrick(h=1, w=1, x=0, y=0, z=1)])
        result = self.solver.solve(structure)
        self.assertEqual(len(result.bricks), 0)

    def test_vertical_stack_stable(self):
        bricks = [
            LegoBrick(h=1, w=1, x=0, y=0, z=0),
            LegoBrick(h=1, w=1, x=0, y=0, z=1),
        ]
        structure = SimpleStructure(bricks)
        result = self.solver.solve(structure)
        self.assertEqual(len(result.bricks), 2)

    def test_overhang_removed(self):
        bricks = [
            LegoBrick(h=1, w=1, x=0, y=0, z=0),
            LegoBrick(h=1, w=2, x=0, y=0, z=1),
        ]
        structure = SimpleStructure(bricks)
        result = self.solver.solve(structure)
        # Top brick should be removed due to overhang
        self.assertEqual(len(result.bricks), 1)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
