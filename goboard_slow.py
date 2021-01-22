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


class GoString:
    """
    To keep track of connected stones of the same colour, and their liberties.
    """

    def __init__(self, colour, stones, liberties):
        self.colour = colour
        self.stones = set(stones)
        self.liberties = set(liberties)

    def remove_liberty(self, point):
        """
        A liberty is removed when opponents play next to this string.
        """
        self.liberties.remove(point)

    def add_liberty(self, point):
        """
        A liberty is added when stones adjacent to this string are captured.
        """
        self.liberties.add(point)

    def merged_with(self, go_string):
        """
        Called when a player connects two of its groups by placing a stone.
        """
        assert go_string.colour == self.colour
        combined_stones = self.stones | go_string.stones
        return GoString(
            self.colour,
            combined_stones,
            (self.liberties | go_string.liberties) - combined_stones,
        )

    @property
    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self, other):
        return (
            isinstance(other, GoString)
            and self.colour == other.colour
            and self.stones == other.stones
            and self.liberties == other.liberties
        )
