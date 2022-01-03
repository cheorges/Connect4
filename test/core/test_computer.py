import unittest

from connect4.core.board import Board
from connect4.core.computer import Computer
from connect4.core.player import playerX, N, X, O, playerO


class TestGame(unittest.TestCase):

    def test_is_terminal_node_player_x_win(self):
        board = Board([[X, X, X, X, N, X, X, X],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N]])
        computer = Computer(playerX, playerO)
        self.assertEqual(computer.minimax(board, 0, 0, 0, False)[1], 100000000)

    def test_is_terminal_node_player_o_win(self):
        board = Board([[O, O, O, O, N, X, X, X],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N]])
        computer = Computer(playerX, playerO)
        self.assertEqual(computer.minimax(board, 0, 0, 0, False)[1], -100000000)

    def test_is_terminal_node_tied(self):
        board = Board([[O, X, O, O, X, O, O, X],
                       [O, O, X, X, O, X, O, X],
                       [O, X, O, O, X, O, O, X],
                       [X, O, X, X, O, X, X, O],
                       [O, X, O, X, X, O, O, X],
                       [X, O, X, X, O, O, X, O],
                       [O, X, O, O, X, X, O, X]])
        computer = Computer(playerX, playerO)
        self.assertEqual(computer.minimax(board, 0, 0, 0, False)[1], 0)

    def test_make_traps_for_the_opponent_col(self):
        board = Board([[N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, O, N, N, N, N],
                       [N, N, N, O, N, N, N, N],
                       [N, N, N, O, N, N, N, N]])
        computer = Computer(playerX, playerO)
        self.assertEqual(computer.minimax(board)[0], 3)

    def test_make_traps_for_the_opponent_row(self):
        board = Board([[N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, O, O, O, N, N, N],
                       [N, N, X, X, X, O, N, N],
                       [N, N, O, X, X, O, N, N]])
        computer = Computer(playerX, playerO)
        self.assertEqual(computer.minimax(board)[0], 5)

    def test_make_traps_for_the_opponent_vertical_down_top(self):
        board = Board([[N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, O, N, N],
                       [N, N, O, N, O, X, N, N],
                       [N, N, X, N, X, O, N, N],
                       [N, N, O, X, X, O, N, N]])
        computer = Computer(playerX, playerO)
        self.assertEqual(computer.minimax(board)[0], 3)

    def test_make_traps_for_the_opponent_vertical_top_down(self):
        board = Board([[N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, O, N, N],
                       [N, N, N, X, O, X, N, N],
                       [N, N, N, O, X, O, N, N],
                       [N, N, N, X, X, O, N, N]])
        computer = Computer(playerX, playerO)
        self.assertEqual(computer.minimax(board)[0], 2)

    def test_find_winning_move_col(self):
        board = Board([[N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, X, N, N, N, N],
                       [N, N, N, X, N, N, N, N],
                       [N, N, N, X, N, N, N, N]])
        computer = Computer(playerX, playerO)
        self.assertEqual(computer.minimax(board)[0], 3)

    def test_find_winning_move_row(self):
        board = Board([[N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, O, O, N, N, N],
                       [N, O, X, X, X, N, N, N],
                       [N, O, O, X, X, O, N, N]])
        computer = Computer(playerX, playerO)
        self.assertEqual(computer.minimax(board)[0], 5)

    def test_find_winning_move__vertical_down_top(self):
        board = Board([[N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, O, X, O, X, N, N],
                       [N, N, X, O, X, O, N, N],
                       [N, X, O, X, X, O, N, N]])
        computer = Computer(playerX, playerO)
        self.assertEqual(computer.minimax(board)[0], 4)

    def test_find_winning_move_vertical_top_down(self):
        board = Board([[N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, N, N, N, N, N, N],
                       [N, N, X, N, N, O, N, N],
                       [N, N, O, N, O, X, N, N],
                       [N, N, O, O, X, O, N, N],
                       [N, N, X, O, X, X, N, N]])
        computer = Computer(playerX, playerO)
        self.assertEqual(computer.minimax(board)[0], 3)


if __name__ == '__main__':
    unittest.main()
