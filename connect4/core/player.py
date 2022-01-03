X = (255, 0, 0)
WX = (255, 128, 128)
O = (255, 255, 0)
WO = (0, 255, 0)
N = (0, 0, 0)


class Player(object):

    def __init__(self, name: str, color: tuple, win_color: tuple):
        self.__name = name
        self.__color = color
        self.__win_color = win_color

    @property
    def name(self) -> str:
        return self.__name

    @property
    def color(self) -> tuple:
        return self.__color

    @property
    def win_color(self) -> tuple:
        return self.__win_color

    def is_piece(self, piece: tuple) -> bool:
        return self.__color == piece or self.__win_color == piece

    def __eq__(self, other) -> bool:
        if isinstance(other, Player):
            return self.name == other.name
        return False

    def __repr__(self) -> str:
        return self.name


playerX = Player("Player 1", X, WX)
playerO = Player("Player 2", O, WO)
