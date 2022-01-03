import math
from abc import ABC, abstractmethod

from connect4.core.board import BoardState
from connect4.core.computer import Computer
from connect4.core.game import Game
from connect4.core.player import playerX, playerO
from connect4.integration.observer import Observer


class Controller(ABC):

    def __init__(self, observer: Observer):
        self._game_over = False
        self._current_player = playerX
        self._game = Game(self._current_player)
        self._observer = observer
        self._observer.show_board(self._game.board_flatten())

    @property
    def game_over(self) -> bool:
        return self._game_over

    def go_right(self) -> None:
        self._game.cursor_right(self._current_player)
        self._observer.show_board(self._game.board_flatten())

    def go_left(self) -> None:
        self._game.cursor_left(self._current_player)
        self._observer.show_board(self._game.board_flatten())

    def insert(self) -> None:
        if self._game.insert(self._current_player, self._game.cursor_pos):
            self._observer.drop_piece(self._game.current_board_col(), self._current_player)
            self._observer.show_board(self._game.board_flatten())
            self.handle(self._game.check_for(self._current_player))

    def restart(self) -> None:
        self._game_over = False
        self._current_player = playerO if self._current_player == playerX else playerX
        self._game = Game(self._current_player)
        self._observer.show_board(self._game.board_flatten())

    @abstractmethod
    def handle(self, state: BoardState) -> None:
        pass


class PvPGameController(Controller):

    def __init__(self, observer: Observer):
        Controller.__init__(self, observer)
        self.__event = {
            BoardState.FREE: self.__change_player,
            BoardState.VICTORY: self.__show_winner,
            BoardState.FULL: self.__show_tied
        }

    def handle(self, state: BoardState) -> None:
        self.__event[state]()

    def __change_player(self) -> None:
        self._current_player = playerO if self._current_player == playerX else playerX
        self._game.change(self._current_player)
        self._observer.show_board(self._game.board_flatten())

    def __show_winner(self) -> None:
        self._observer.show_board(self._game.board_flatten())
        self._observer.show_winner(self._current_player)
        self._game_over = True

    def __show_tied(self) -> None:
        self._observer.show_board(self._game.board_flatten())
        self._observer.game_end_with_tied()
        self._game_over = True


class PvCGameController(Controller, Computer):

    def __init__(self, observer: Observer):
        Controller.__init__(self, observer)
        Computer.__init__(self, playerO, playerX)
        self.__event = {
            BoardState.FREE: self.__change_player,
            BoardState.VICTORY: self.__show_winner,
            BoardState.FULL: self.__show_tied
        }

    def handle(self, state: BoardState) -> None:
        self.__event[state]()

    def __change_player(self) -> None:
        self._current_player = playerO if self._current_player == playerX else playerX
        self._game.change(self._current_player)
        self.__insert_if_computer()

    def __show_winner(self) -> None:
        self._observer.show_board(self._game.board_flatten())
        self._observer.show_winner(self._current_player)
        self._game_over = True

    def __show_tied(self) -> None:
        self._observer.show_board(self._game.board_flatten())
        self._observer.game_end_with_tied()
        self._game_over = True

    def restart(self) -> None:
        self._game_over = False
        self._current_player = playerO if self._current_player == playerX else playerX
        self._game = Game(self._current_player)
        self._observer.show_board(self._game.board_flatten())
        self.__insert_if_computer()

    def __insert_if_computer(self) -> None:
        if self._current_player == playerO:
            while True:
                self._observer.show_board(self._game.board_flatten())
                col = self.minimax(self._game, 4, -math.inf, math.inf, True)[0]
                self._observer.move_cursor_to_specific_pos(self._game.cursor_pos, col, self._current_player)
                if self._game.insert(self._current_player, col):
                    self._observer.drop_piece(self._game.specific_board_col(col), self._current_player)
                    self.handle(self._game.check_for(self._current_player))
                    break
        else:
            self._observer.show_board(self._game.board_flatten())
