from dataclasses import dataclass
from Constants import FILE_SIZE, RANK_SIZE, SQUARE_PX
import string

@dataclass(frozen=True)
class Position:
    """
    Position on the board.
    x and y are 0 based indices.
    """
    x: int
    y: int


    @classmethod
    def algebraic(cls, coord: str):
        if len(coord) != 2:
            raise ValueError('Invalid coordinate')

        file, rank = coord.lower()
        if file in string.ascii_lowercase[:FILE_SIZE] and 1 <= int(rank) <= RANK_SIZE:
            x = ord(file) - ord('a')
            y = int(rank) - 1
            return cls(x, y)

        else:
            raise ValueError('Invalid coordinate')


    def in_bounds(self):
        """check if a position is within the board"""
        return 0 <= self.x < FILE_SIZE and 0 <= self.y < RANK_SIZE


    def pos_on_canvas(self):
        x = self.x * SQUARE_PX + SQUARE_PX / 2
        y = self.y * SQUARE_PX + SQUARE_PX / 2
        return x, y