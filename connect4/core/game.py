from connect4.core.board import Board
from connect4.core.player import Player, N


class Game(Board):

    def __init__(self, player: Player, current_col: int = 0):
        Board.__init__(self)
        self.__current_col = current_col
        self.__input_cols = [(N) for _ in range(self.MAX_COL)]
        self.__input_cols[current_col] = player.color

    @property
    def cursor_pos(self) -> int:
        return self.__current_col

    def cursor_right(self, player: Player) -> None:
        self.__input_cols[self.cursor_pos] = N
        self.__current_col = 0 if self.cursor_pos == self.MAX_COL - 1 else self.cursor_pos + 1
        self.__input_cols[self.cursor_pos] = player.color

    def cursor_left(self, player: Player) -> None:
        self.__input_cols[self.cursor_pos] = N
        self.__current_col = self.MAX_COL - 1 if self.cursor_pos == 0 else self.cursor_pos - 1
        self.__input_cols[self.cursor_pos] = player.color

    def change(self, player: Player) -> None:
        self.__input_cols[self.cursor_pos] = player.color

    def board_flatten(self) -> list:
        game_grid_flat = [self.__input_cols[pos] for pos in range(self.MAX_COL)]
        for row in self.game_grid_copy:
            for element in row:
                game_grid_flat.append(element)
        return game_grid_flat

    def current_board_col(self) -> tuple:
        return self.cursor_pos, self.current_col(self.cursor_pos)

    def specific_board_col(self, col) -> tuple:
        return col, self.current_col(col)
