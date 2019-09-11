from enum import IntEnum
import re


class Field(IntEnum):
    NONE = 0
    X = 1
    O = 2


class BoardState:

    def __init__(self):
        self.state = [Field.NONE for i in range(9)]

    @classmethod
    def from_int(cls, i):
        assert len(str(i)) == 9, "Integer has field length of 9."
        assert len(re.sub("[^012]+", "", str(i))
                   ) == 9, "Integer only has characters 0, 1, 2."
        c = cls()
        c.state = [int(element) for element in str(i)]
        return c

    def to_int(self):
        return int("".join(map(str, self.state)))

    def set_field(self, i, field: Field):
        self.state[i] = int(field)

    def get_field(self, i):
        return self.state[i]

    def __repr__(self):
        board_formated = [" " if e == Field(0).name else e for e in [
            Field(i).name for i in self.state]]
        s = "+---+---+---+\n"    \
            "| {} | {} | {} |\n" \
            "+---+---+---+\n"    \
            "| {} | {} | {} |\n" \
            "+---+---+---+\n"    \
            "| {} | {} | {} |\n" \
            "+---+---+---+".format(*board_formated)

        return s
