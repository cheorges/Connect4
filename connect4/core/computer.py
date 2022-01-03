import math
import os
import random
from copy import deepcopy

from connect4.core.board import Board, BoardState
from connect4.core.player import Player, N


def difficult_connect_4() -> int:
    return os.environ.get('DIFFICULT_CONNECT_4') or 3


class Computer(object):
    LENGTH = 4

    def __init__(self, ai_player: Player, player: Player):
        self.ai_player = ai_player
        self.player = player

    def minimax(self, board: Board,
                depth: int = difficult_connect_4(),
                alpha: float = -math.inf,
                beta: float = math.inf,
                maximizing_player: bool = True) -> tuple:
        valid_locations = board.valid_positions()
        is_terminal = self.__is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if board.check_for(self.ai_player) is BoardState.VICTORY:
                    return None, 100000000
                elif board.check_for(self.player) is BoardState.VICTORY:
                    return None, -100000000
                else:
                    return None, 0
            else:
                return None, self.__score_position(board, self.ai_player)
        if maximizing_player:
            return self.__maximizing(board, depth, alpha, beta, valid_locations)
        else:
            return self.__minimizing(board, depth, alpha, beta, valid_locations)

    def __minimizing(self, board: Board, depth: int, alpha: float, beta: float, valid_locations: list) -> tuple:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = deepcopy(board)
            b_copy.insert(self.player, col)
            new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

    def __maximizing(self, board: Board, depth: int, alpha: float, beta: float, valid_locations: list) -> tuple:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = deepcopy(board)
            b_copy.insert(self.ai_player, col)
            new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    def __is_terminal_node(self, board: Board) -> bool:
        return board.check_for(self.player) is not BoardState.FREE or \
               board.check_for(self.ai_player) is not BoardState.FREE or \
               len(board.valid_positions()) == 0

    def __score_position(self, board: Board, player: Player) -> int:
        score = 0
        score += board.current_row(board.MAX_ROW // 2).count(player.color) * 3

        for row_index in range(board.MAX_ROW):
            row = board.current_row(row_index)
            for col_index in range(board.MAX_COL - 3):
                scope = row[col_index:col_index + self.LENGTH]
                score += self.__rating_scope(scope, player)

        for col_index in range(board.MAX_COL):
            col = board.current_col(col_index)
            for row_index in range(board.MAX_ROW - 3):
                scope = col[row_index:row_index + self.LENGTH]
                score += self.__rating_scope(scope, player)

        for row_index in range(board.MAX_ROW - 3):
            for col_index in range(board.MAX_COL - 3):
                scope = [board.game_grid_copy[row_index + i][col_index + i] for i in range(self.LENGTH)]
                score += self.__rating_scope(scope, player)

        for row_index in range(board.MAX_ROW - 3):
            for col_index in range(board.MAX_COL - 3):
                scope = [board.game_grid_copy[row_index + 3 - i][col_index + i] for i in range(self.LENGTH)]
                score += self.__rating_scope(scope, player)

        return score

    def __rating_scope(self, scope: list, player: Player) -> int:
        score = 0
        ai_player = self.ai_player if player == self.player else self.player
        if scope.count(player.color) == 4:
            score += 100
        elif scope.count(player.color) == 3 and scope.count(N) == 1:
            score += 5
        elif scope.count(player.color) == 2 and scope.count(N) == 2:
            score += 2
        if scope.count(ai_player.color) == 3 and scope.count(N) == 1:
            score -= 4
        return score
