import unittest
from backend.inventory import filter_counts, load_inventory

class InventoryTests(unittest.TestCase):
    def test_filter_excess(self):
        counts = {"3001.DAT": 5, "3003.DAT": 2}
        inv = {"3001.DAT": 3, "3003.DAT": 2}
        # patch inventory loader
        from backend import inventory as inv_mod
        inv_mod._INVENTORY = inv
        filtered = filter_counts(counts)
        self.assertEqual(filtered, {"3001.DAT": 3, "3003.DAT": 2})

    def test_filter_missing(self):
        counts = {"3001.DAT": 1, "9999.DAT": 2}
        inv = {"3001.DAT": 5}
        from backend import inventory as inv_mod
        inv_mod._INVENTORY = inv
        filtered = filter_counts(counts)
        self.assertEqual(filtered, {"3001.DAT": 1})


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

