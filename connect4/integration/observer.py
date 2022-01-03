from abc import ABC, abstractmethod

from connect4.core.player import Player


class Observer(ABC):

    @abstractmethod
    def show_board(self, board: list) -> None:
        pass

    @abstractmethod
    def drop_piece(self, current_col: tuple, player: Player) -> None:
        pass

    @abstractmethod
    def show_winner(self, player: Player) -> None:
        pass

    @abstractmethod
    def move_cursor_to_specific_pos(self, cursor_pos: int, target_pos: int, player: Player) -> None:
        pass

    @abstractmethod
    def game_end_with_tied(self) -> None:
        pass
