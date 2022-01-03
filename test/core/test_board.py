import unittest

from connect4.core.board import Board, BoardState
from connect4.core.player import playerX, X, N, O


class BoardTest(unittest.TestCase):

    def test_insert_is_not_possible(self):
        board = Board([[X, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N]])
        self.assertFalse(board.insert(playerX, 0))

    def test_return_valid_psitions(self):
        board = Board([[X, O, N, X, N, N, O, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N]])
        positions = board.valid_positions()
        self.assertEqual(positions, [2, 4, 5, 7])

    def test_insert(self):
        board = Board([[N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N]])
        board.insert(playerX, 0)
        self.assertEqual(board.game_grid_copy,
                         [[N, N, N, N, N, N, N, N],
                          [N, N, N, N, N, N, N, N],
                          [N, N, N, N, N, N, N, N],
                          [N, N, N, N, N, N, N, N],
                          [N, N, N, N, N, N, N, N],
                          [N, N, N, N, N, N, N, N],
                          [X, N, N, N, N, N, N, N]])

    def test_four_connected_in_row(self):
        board = Board([[N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, X, X, X, X, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N]])
        self.assertEqual(board.check_for(playerX), BoardState.VICTORY)

    def test_four_connected_in_col(self):
        board = Board([[N, N, N, N, N, N, N, N],
                       [N, N, N, X, N, N, N, N],
                       [N, N, N, X, N, N, N, N],
                       [N, N, N, X, N, N, N, N],
                       [N, N, N, X, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N]])
        self.assertEqual(board.check_for(playerX), BoardState.VICTORY)

    def test_four_connected_in_vertical_top_down(self):
        board = Board([[N, N, N, N, N, N, N, N],
                       [N, N, N, X, N, N, N, N],
                       [N, N, N, N, X, N, N, N],
                       [N, N, N, N, N, X, N, N],
                       [N, N, N, N, N, N, X, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N]])
        self.assertEqual(board.check_for(playerX), BoardState.VICTORY)

    def test_four_connected_in_vertical_down_top(self):
        board = Board([[N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, X],
                       [N, N, N, N, N, N, X, N],
                       [N, N, N, N, N, X, N, N],
                       [N, N, N, N, X, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N]])
        self.assertEqual(board.check_for(playerX), BoardState.VICTORY)

    def test_has_free_space(self):
        board = Board([[N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N]])
        self.assertEqual(board.check_for(playerX), BoardState.FREE)

    def test_has_no_free_space(self):
        board = Board([[O, X, O, O, O, X, O, X],
                       [X, O, X, X, O, X, X, X],
                       [O, X, O, O, X, O, O, X],
                       [X, O, X, X, O, X, X, O],
                       [O, X, O, O, X, O, O, X],
                       [X, O, X, X, X, O, X, O],
                       [O, X, O, O, O, X, O, X]])
        self.assertEqual(board.check_for(playerX), BoardState.FULL)

    def test_get_current_col_with_index(self):
        board = Board([[O, X, O, O, O, X, O, X],
                       [X, O, X, X, O, X, X, X],
                       [O, X, O, O, X, O, O, X],
                       [X, O, X, X, O, X, X, O],
                       [O, X, O, O, X, O, O, X],
                       [X, O, X, X, X, O, X, O],
                       [O, X, O, O, O, X, O, X]])
        self.assertEqual(board.current_col(0), [O, X, O, X, O, X, O])
        self.assertEqual(board.current_col(1), [X, O, X, O, X, O, X])
        self.assertEqual(board.current_col(2), [O, X, O, X, O, X, O])
        self.assertEqual(board.current_col(3), [O, X, O, X, O, X, O])
        self.assertEqual(board.current_col(4), [O, O, X, O, X, X, O])
        self.assertEqual(board.current_col(5), [X, X, O, X, O, O, X])
        self.assertEqual(board.current_col(6), [O, X, O, X, O, X, O])
        self.assertEqual(board.current_col(7), [X, X, X, O, X, O, X])

    def test_get_current_row_with_index(self):
        board = Board([[O, X, O, O, O, X, O, X],
                       [X, O, X, X, O, X, X, X],
                       [O, X, O, O, X, O, O, X],
                       [X, O, X, X, O, X, X, O],
                       [O, X, O, O, X, O, O, X],
                       [X, O, X, X, X, O, X, O],
                       [O, X, O, O, O, X, O, X]])
        self.assertEqual(board.current_row(0), [O, X, O, O, O, X, O, X])
        self.assertEqual(board.current_row(1), [X, O, X, X, O, X, X, X])
        self.assertEqual(board.current_row(2), [O, X, O, O, X, O, O, X])
        self.assertEqual(board.current_row(3), [X, O, X, X, O, X, X, O])
        self.assertEqual(board.current_row(4), [O, X, O, O, X, O, O, X])
        self.assertEqual(board.current_row(5), [X, O, X, X, X, O, X, O])
        self.assertEqual(board.current_row(6), [O, X, O, O, O, X, O, X])


if __name__ == '__main__':
    unittest.main()
