import unittest

from boardtypes import *


class InterfaceTests(unittest.TestCase):
    def test_equality(self):
        board1 = TileBoard(8)
        board2 = TileBoard(8, board1.state_tuple())
        self.assertTrue(board1 == board2)

    def test_solved(self):
        state = (1, 2, 3, 4, None, 5, 6, 7, 8)
        board = TileBoard(8, state)
        self.assertTrue(board.solved())

    def test_unsolved(self):
        state = (8, 7, 6, 5, None, 4, 3, 2, 1)
        board = TileBoard(8, state)
        self.assertFalse(board.solved())


if __name__ == '__main__':
    unittest.main()
