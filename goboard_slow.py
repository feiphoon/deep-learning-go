from collections import namedtuple


class Point(namedtuple("Point", "row col")):
    def neighbours(self):
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]


class Move:
    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert (
            (point is not None) ^ is_pass ^ is_resign
        )  #  ^ XOR - if one and only one of these are true
        self.point = point
        self.is_play = self.point is not None
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point):
        return Move(point=point)

    @classmethod
    def pass_turn(cls):
        return Move(is_pass=True)

    @classmethod
    def resign(cls):
        return Move(is_resign=True)
