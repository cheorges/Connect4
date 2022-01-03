import time
from enum import Enum

from sense_hat import SenseHat, ACTION_PRESSED

from connect4.app import App
from connect4.core.player import Player, N, playerO, playerX
from connect4.integration.controller import PvCGameController, PvPGameController
from connect4.integration.observer import Observer

RIGHT = "right"
LEFT = "left"
MIDDLE = "middle"
UP = "up"
DOWN = "down"


class GameMode(Enum):
    PVP = "P"
    PVC = "C"


class BestOf(Enum):
    ONE = 1
    THREE = 3
    FIVE = 5
    SEVEN = 7

    def next(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) + 1
        if index >= len(members):
            return members[0]
        return members[index]

    def prev(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) - 1
        if index < 0:
            return members[-1]
        return members[index]


class Raspberry(App):

    def run(self):
        Menu()


class Connect4(Observer, SenseHat):

    def __init__(self, best_of: int, mode: GameMode):
        SenseHat.__init__(self)
        self.__controller = PvPGameController(self) if mode == GameMode.PVP else PvCGameController(self)
        self.__win_series = best_of // 2 + 1
        self.__best_of = {playerX.name: self.__win_series, playerO.name: self.__win_series}
        self.__actions = {
            RIGHT: self.__controller.go_right,
            LEFT: self.__controller.go_left,
            MIDDLE: self.__controller.insert
        }
        self.__run()

    def __run(self) -> None:
        while not self.__controller.game_over:
            event = self.stick.wait_for_event()
            if event.action == ACTION_PRESSED and event.direction in self.__actions:
                self.__actions[event.direction]()

    def show_board(self, board: list) -> None:
        self.set_pixels(board)

    def drop_piece(self, current_col: tuple, player: Player) -> None:
        col, rows = current_col
        for index in range(rows.__len__()):
            if index == rows.__len__() - 1 or rows[index + 1] != N:
                break
            else:
                self.set_pixel(col, index, N)
                self.set_pixel(col, index + 1, player.color)
                time.sleep(0.05)

    def move_cursor_to_specific_pos(self, cursor_pos: int, target_pos: int, player: Player) -> None:
        while cursor_pos != target_pos:
            self.set_pixel(cursor_pos, 0, N)
            if cursor_pos > target_pos:
                cursor_pos -= 1
                self.__controller.go_left()
            else:
                cursor_pos += 1
                self.__controller.go_right()
            self.set_pixel(cursor_pos, 0, player.color)
            time.sleep(0.05)

    def show_winner(self, player: Player) -> None:
        time.sleep(3)
        self.__best_of[player.name] = self.__best_of[player.name] - 1
        self.show_letter(str(self.__win_series - self.__best_of[playerX.name]), playerX.color)
        time.sleep(1.5)
        self.show_letter(str(self.__win_series - self.__best_of[playerO.name]), playerO.color)
        time.sleep(1.5)
        if self.__best_of[player.name] == 0:
            self.__show_trophy(player)
            Menu()
        else:
            self.__controller.restart()
            self.__run()

    def game_end_with_tied(self) -> None:
        time.sleep(3)
        self.show_message(f"Tied", text_colour=(255, 255, 255))

    def __show_trophy(self, player):
        c = player.color
        self.set_pixels([N, N, N, N, N, N, N, N,
                         N, N, c, c, c, c, N, N,
                         c, c, c, c, c, c, c, c,
                         c, N, c, c, c, c, N, c,
                         N, c, c, c, c, c, c, N,
                         N, N, N, c, c, N, N, N,
                         N, N, N, c, c, N, N, N,
                         N, c, c, c, c, c, c, N
                         ])
        time.sleep(2)


class Menu(SenseHat):

    def __init__(self):
        SenseHat.__init__(self)
        self.__mode = GameMode.PVP
        self.__best_of = BestOf.ONE
        self.__mode_actions = {
            UP: self.__toggle_mode,
            DOWN: self.__toggle_mode,
            MIDDLE: self.__confirm_mode,
        }
        self.__best_of_mode_actions = {
            UP: self.__increment_best_of_mode,
            DOWN: self.__decrement_best_of_mode,
            MIDDLE: self.__start_game,
            LEFT: self.__start,
        }
        self.show_message(f"Connect 4", text_colour=(255, 255, 255))
        self.__start()

    def __start(self):
        self.show_letter(f"{self.__mode.value}", text_colour=(0, 255, 255))
        while True:
            event = self.stick.wait_for_event()
            if event.action == ACTION_PRESSED and (event.direction in [UP, DOWN, MIDDLE]):
                self.__mode_actions[event.direction]()

    def __toggle_mode(self):
        self.__mode = GameMode.PVP if self.__mode == GameMode.PVC else GameMode.PVC
        self.show_letter(f"{self.__mode.value}", text_colour=(0, 255, 255))

    def __confirm_mode(self):
        self.show_letter(f"{self.__best_of.value}", text_colour=(255, 0, 255))
        while True:
            event = self.stick.wait_for_event()
            if event.action == ACTION_PRESSED and (event.direction == UP or event.direction == DOWN):
                self.__best_of_mode_actions[event.direction]()
                self.show_letter(f"{self.__best_of.value}", text_colour=(255, 0, 255))
            if event.action == ACTION_PRESSED and (event.direction == MIDDLE or event.direction == LEFT):
                self.__best_of_mode_actions[event.direction]()

    def __increment_best_of_mode(self):
        self.__best_of = self.__best_of.next()

    def __decrement_best_of_mode(self):
        self.__best_of = self.__best_of.prev()

    def __start_game(self):
        Connect4(self.__best_of.value, self.__mode)
