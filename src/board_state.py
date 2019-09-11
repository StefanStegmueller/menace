from enum import IntEnum
from functools import reduce
import re


class Field(IntEnum):
    NONE = 0
    X = 1
    O = 2


class Result(IntEnum):
    NONE = 0
    X_WINS = 1
    O_WINS = 2
    DRAW = 3


class BoardState:

    def __init__(self):
        self.board = [0 for i in range(9)]

    @classmethod
    def from_board(cls, board):
        c = cls()
        c.board = board
        return c

    def to_string(self):
        return reduce(lambda x, y: x+str(y), self.board, '')

    def set_field(self, i, field: Field):
        board = self.board.copy()
        board[i] = int(field)
        return BoardState.from_board(board)

    def get_field(self, i):
        return self.board[i]

    def check_winner(self) -> Result:
        if not(Field.NONE in self.board):
            return Result.DRAW

        rows = list(self.__divide_chunks(self.board, 3))
        columns = [[r[i] for r in rows]for i in range(0, 3)]
        diagonals = [[rows[0][0], rows[1][1], rows[2][2]],
                     [rows[0][2], rows[1][1], rows[2][0]]]

        lines_of_interest = rows + columns + diagonals
        for line in lines_of_interest:
            if all(elem == line[0] for elem in line) and line[0] != Field.NONE:
                return Result(line[0])
        return Result.NONE

    def __divide_chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def __repr__(self):
        board_formated = [" " if e == Field(0).name else e for e in [
            Field(i).name for i in self.board]]
        s = "     1   2   3    x\n" \
            "   +---+---+---+\n" \
            " 1 | {} | {} | {} |\n" \
            "   +---+---+---+\n" \
            " 2 | {} | {} | {} |\n" \
            "   +---+---+---+\n" \
            " 3 | {} | {} | {} |\n" \
            "   +---+---+---+\n" \
            " y".format(*board_formated)
        return s
