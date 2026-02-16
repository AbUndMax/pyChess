from dataclasses import dataclass
from Constants import FILE_SIZE, RANK_SIZE, SQUARE_PX
import string

"""
The following interpretations are used:
- file: horizontal direction, given by letters a-h (on 8x8 board)
- rank: vertical direction, given by numbers 1-8 (on 8x8 board)

- file_idx: index of the file, starting from 0 at the bottom left corner
- rank_idx: index of the rank, starting from 0 at the bottom left corner
-> idx values refer to the CENTER of the respective square!
    Thus Position(file_idx, rank_idx) defines a position in the square grid and not a coord
    on the board canvas 

- x and y: coordinates on the board canvas
"""


def calculate_position(x, y):
    """
    takes canvas coordinates and calculates the nearest center of the square on the board
    :param x: the x coordinate on the board canvas
    :param y: the y coordinate on the board canvas
    :return: Position in which x and y lie
    """
    file_idx = x // SQUARE_PX
    rank_idx = y // SQUARE_PX
    return Position(file_idx, rank_idx)



@dataclass(frozen=True)
class Position:
    """
    Position on the board.
    both values are the indices of the square on the board, starting from 0 at the bottom left corner.
    """
    file_idx: int
    rank_idx: int


    @classmethod
    def algebraic(cls, coord: str):
        if len(coord) != 2:
            raise ValueError('Invalid coordinate')

        file, rank = coord.lower()
        if file in string.ascii_lowercase[:FILE_SIZE] and 1 <= int(rank) <= RANK_SIZE:
            file_idx = ord(file) - ord('a')
            rank_idx = int(rank) - 1
            return cls(file_idx, rank_idx)

        else:
            raise ValueError('Invalid coordinate')


    def in_bounds(self):
        """check if a position is within the board"""
        return 0 <= self.file_idx < FILE_SIZE and 0 <= self.rank_idx < RANK_SIZE


    def calculate_board_coords(self):
        """
        calculates the board coordinates of the center for the square this instance represents
        :return: x, y coordinates of the center of the square
        """
        x = self.file_idx * SQUARE_PX + SQUARE_PX / 2
        y = self.rank_idx * SQUARE_PX + SQUARE_PX / 2
        return x, y