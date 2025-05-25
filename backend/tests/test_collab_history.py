import json
import unittest
from backend.collab import handle_message, _history, _index


class HistoryTests(unittest.TestCase):
    def setUp(self):
        _history.clear()
        _index.clear()

    def test_edit_undo_redo(self):
        room = "r1"
        msg = handle_message(room, json.dumps({"type": "edit", "data": "a"}))
        self.assertEqual(json.loads(msg), {"type": "edit", "data": "a"})
        self.assertEqual(_history[room], ["a"])
        self.assertEqual(_index[room], 1)

        handle_message(room, json.dumps({"type": "edit", "data": "b"}))
        self.assertEqual(_history[room], ["a", "b"])
        self.assertEqual(_index[room], 2)

        undo_msg = handle_message(room, json.dumps({"type": "undo"}))
        self.assertEqual(json.loads(undo_msg), {"type": "undo", "data": "b"})
        self.assertEqual(_index[room], 1)

        redo_msg = handle_message(room, json.dumps({"type": "redo"}))
        self.assertEqual(json.loads(redo_msg), {"type": "redo", "data": "b"})
        self.assertEqual(_index[room], 2)


if __name__ == "__main__":
    unittest.main()
