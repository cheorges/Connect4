from copy import copy
from enum import Enum

from connect4.core.player import N, Player


class BoardState(Enum):
    FULL = 1,
    VICTORY = 2,
    FREE = 3


class Board(object):
    MAX_COL = 8
    MAX_ROW = 7

    def __init__(self, game_grid=None):
        self.__game_grid = [[N] * self.MAX_COL for _ in range(self.MAX_ROW)]
        if game_grid is not None:
            self.__game_grid = game_grid

    @property
    def game_grid_copy(self) -> list:
        return copy(self.__game_grid)

    def check_for(self, player: Player) -> BoardState:
        if self.__check_row_for_win(player) or \
                self.__check_col_for_win(player) or \
                self.__check_diagonal_for_win(player):
            return BoardState.VICTORY
        if self.__free_space():
            return BoardState.FREE
        return BoardState.FULL

    def __check_row_for_win(self, player: Player) -> bool:
        for col in range(self.MAX_COL - 3):
            for row in reversed(range(self.MAX_ROW)):
                if player.is_piece(self.__game_grid[row][col]) and \
                        player.is_piece(self.__game_grid[row][col + 1]) and \
                        player.is_piece(self.__game_grid[row][col + 2]) and \
                        player.is_piece(self.__game_grid[row][col + 3]):
                    for i in range(4):
                        self.__game_grid[row][col + i] = player.win_color
                    return True
        return False

    def __check_col_for_win(self, player: Player) -> bool:
        for col in range(self.MAX_COL):
            for row in reversed(range(self.MAX_ROW - 3)):
                if player.is_piece(self.__game_grid[row][col]) and \
                        player.is_piece(self.__game_grid[row + 1][col]) and \
                        player.is_piece(self.__game_grid[row + 2][col]) and \
                        player.is_piece(self.__game_grid[row + 3][col]):
                    for i in range(4):
                        self.__game_grid[row + i][col] = player.win_color
                    return True
        return False

    def __check_diagonal_for_win(self, player: Player) -> bool:
        for col in range(self.MAX_COL - 3):
            for row in reversed(range(self.MAX_ROW - 3)):
                if player.is_piece(self.__game_grid[row][col]) and \
                        player.is_piece(self.__game_grid[row + 1][col + 1]) and \
                        player.is_piece(self.__game_grid[row + 2][col + 2]) and \
                        player.is_piece(self.__game_grid[row + 3][col + 3]):
                    for i in range(4):
                        self.__game_grid[row + i][col + i] = player.win_color
                    return True
        for col in range(self.MAX_COL - 3):
            for row in reversed(range(4, self.MAX_ROW)):
                if player.is_piece(self.__game_grid[row][col]) and \
                        player.is_piece(self.__game_grid[row - 1][col + 1]) and \
                        player.is_piece(self.__game_grid[row - 2][col + 2]) and \
                        player.is_piece(self.__game_grid[row - 3][col + 3]):
                    for i in range(4):
                        self.__game_grid[row - i][col + i] = player.win_color
                    return True
        return False

    def __free_space(self) -> bool:
        for col in range(self.MAX_COL):
            for row in reversed(range(self.MAX_ROW - 3)):
                if self.__game_grid[row][col] is N:
                    return True
        return False

    def __insert_possible(self, col) -> bool:
        return True if self.__game_grid[0][col] is N else False

    def insert(self, player: Player, col: int) -> bool:
        if self.__insert_possible(col):
            for row in reversed(range(self.MAX_ROW)):
                if self.__game_grid[row][col] is N:
                    self.__game_grid[row][col] = player.color
                    return True
        return False

    def current_col(self, index: int) -> list:
        return [self.__game_grid[row][index] for row in range(self.MAX_ROW)]

    def current_row(self, index: int) -> list:
        return [self.__game_grid[index][col] for col in range(self.MAX_COL)]

    def valid_positions(self) -> list:
        return [col for col in range(self.MAX_COL) if self.__insert_possible(col)]
