import unittest

from connect4.core.game import Game
from connect4.core.player import X, O, N, playerO, playerX


class TestGame(unittest.TestCase):

    def test_go_right(self):
        game = Game(playerX)
        game.cursor_right(playerX)
        self.assertEqual(game.board_flatten(),
                         [N, X, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N])

    def test_go_right_over_rights_end(self):
        game = Game(playerX, current_col=7)
        game.cursor_right(playerX)
        self.assertEqual(game.board_flatten(),
                         [X, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N])

    def test_go_left(self):
        game = Game(playerX, current_col=7)
        game.cursor_left(playerX)
        self.assertEqual(game.board_flatten(),
                         [N, N, N, N, N, N, X, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N])

    def test_go_left_over_left_end(self):
        game = Game(playerX)
        game.cursor_left(playerX)
        self.assertEqual(game.board_flatten(),
                         [N, N, N, N, N, N, N, X,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N])

    def test_game_init(self):
        game = Game(playerX)
        self.assertEqual(game.board_flatten(),
                         [X, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N])

    def test_change_player(self):
        game = Game(playerX)
        game.change(playerO)
        self.assertEqual(game.board_flatten(),
                         [O, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N,
                          N, N, N, N, N, N, N, N])


if __name__ == '__main__':
    unittest.main()
