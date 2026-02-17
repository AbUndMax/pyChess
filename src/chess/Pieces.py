from abc import ABC, abstractmethod
from typing import Iterable

from Constants import RANK_SIZE, FILE_SIZE, IMG_PATHS
from chess.Position import Position
import tkinter as tk


DIRECTIONS = {
    "l": (-1, 0),
    "r": (1, 0),
    "u": (0, 1),
    "d": (0, -1),
    "lu": (-1, 1),
    "ld": (-1, -1),
    "ru": (1, 1),
    "rd": (1, -1)
}


class Piece(ABC):

    def __init__(self, pos: Position, color: str, board, img_path):
        if color not in ["b", "w"]:
            raise ValueError('Invalid color')

        self.board = board
        self.pos: Position = pos
        self.in_start_pos = True
        self.color: str = color
        self.img = tk.PhotoImage(file=img_path)
        self.item_id_on_board: int = board.draw_piece(self)


    @property
    def moves(self) -> Iterable[Position]:
        yield from self._calculate_moves()


    def new_pos_possible(self, new_pos: Position):
        """
        generates a state code of the new position:
        # 0 = blocked by own color / out of bounds
        # 1 = free
        # 2 = capture (new_pos held by enemy color)

        :param new_pos: the position to check
        :return: 0, 1 or 2
        """
        if not new_pos.in_bounds():
            return 0

        if occupying_piece := self.board.pos_occupied_by(new_pos):
            if occupying_piece.color == self.color:
                return 0
            if occupying_piece.color != self.color:
                return 2

        return 1

    def can_move(self, new_pos: Position) -> bool:
        """
        checks if a given position is a valid move for this piece
        :param new_pos: the position to check
        :return: True if the position is a valid move, False otherwise
        """
        return new_pos in self.moves


    @abstractmethod
    def _calculate_moves(self) -> Iterable[Position]:
        """yield candidate move for this piece in current position"""
        ...


    def _calculate_ray_moves(self, directions) -> Iterable[Position]:
        """
        Calculates possible ray moves based on the provided directions. A ray move represents a
        continuous movement in a given direction until an obstruction or limit is encountered.
        The function stops generating moves in a particular direction when it encounters a position
        that is either blocked by a piece of the same color, goes out of bounds, or results in a
        capture.

        :param directions: Iterable of tuples, where each tuple represents a direction as (dx, dy),
                           indicating changes in file and rank, respectively.
        :return: Iterable of `Position` objects corresponding to valid ray moves in the specified
                 directions.
        """
        for dx, dy in directions:
            for step in range(1, max(FILE_SIZE, RANK_SIZE)):
                new_pos = Position(self.pos.file_idx + dx * step, self.pos.rank_idx + dy * step)

                possible_code = self.new_pos_possible(new_pos)
                match possible_code:
                    case 0: # blocked by own color / out of bounds
                        break # end pos search in this direction
                    case 1: # free
                        yield new_pos
                    case 2: # capture -> add capture move and end search in this direction
                        yield new_pos
                        break


    def can_capture(self, pos_to_capture: Position) -> bool:
        """
        Determines if a capture is possible at the specified position. A capture is only valid if the
        position is occupied by a piece of a different color.

        :param pos_to_capture: The position to check for a possible capture.
        :return: True if the position is occupied by an opponent's piece and can be captured, otherwise False.
        """
        occupant = self.board.pos_occupied_by(pos_to_capture)
        return occupant is not None and occupant.color != self.color


    def move_to(self, new_pos: Position):
        """
        update the position of this piece in the board and recalculate possible moves
        :param new_pos:
        :return:
        """
        # check if move is capture:
        if self.can_capture(new_pos):
            self.board.capture_piece(new_pos)

        # remove old position from board
        del self.board.position_to_piece[self.pos]
        # set new position in instance and board
        self.pos = new_pos
        self.board.position_to_piece[new_pos] = self
        self.in_start_pos = False




class King(Piece):

    def __init__(self, pos: Position, color: str, board):
        self.directions = [DIRECTIONS[d] for d in ["l", "r", "u", "d", "lu", "ru", "ld", "rd"]]
        img_path = IMG_PATHS[color + "K"]
        super().__init__(pos, color, board, img_path)

    def _calculate_moves(self) -> Iterable[Position]:
        step = 1
        for dx, dy in self.directions:
            new_pos = Position(self.pos.file_idx + dx * step, self.pos.rank_idx + dy * step)

            if self.new_pos_possible(new_pos):
                yield new_pos


class Queen(Piece):

    def __init__(self, pos: Position, color: str, board):
        self.directions = [DIRECTIONS[d] for d in ["l", "r", "u", "d", "lu", "ru", "ld", "rd"]]
        img_path = IMG_PATHS[color + "Q"]
        super().__init__(pos, color, board, img_path)

    def _calculate_moves(self) -> Iterable[Position]:
        yield from self._calculate_ray_moves(self.directions)


class Bishop(Piece):

    def __init__(self, pos: Position, color: str, board):
        self.directions = [DIRECTIONS[d] for d in ["lu", "ru", "ld", "rd"]]
        img_path = IMG_PATHS[color + "B"]
        super().__init__(pos, color, board, img_path)

    def _calculate_moves(self) -> Iterable[Position]:
        yield from self._calculate_ray_moves(self.directions)



class Knight(Piece):

    def __init__(self, pos: Position, color: str, board):
        self.directions = [DIRECTIONS[d] for d in ["l", "r", "u", "d"]]
        img_path = IMG_PATHS[color + "N"]
        super().__init__(pos, color, board, img_path)

    def _calculate_moves(self) -> Iterable[Position]:
        step = 2
        for dx, dy in self.directions:
            for i in (1, -1):
                new_pos = Position(self.pos.file_idx + dx * step + i * dy, self.pos.rank_idx + dy * step + i * dx)
                if self.new_pos_possible(new_pos):
                    yield new_pos



class Rook(Piece):

    def __init__(self, pos: Position, color: str, board):
        self.directions = [DIRECTIONS[d] for d in ["l", "r", "u", "d"]]
        img_path = IMG_PATHS[color + "R"]
        super().__init__(pos, color, board, img_path)

    def _calculate_moves(self) -> Iterable[Position]:
        yield from self._calculate_ray_moves(self.directions)



class Pawn(Piece):

    def __init__(self, pos: Position, color: str, board):
        self.directions = [DIRECTIONS["u"]] if color == "w" else [DIRECTIONS["d"]]
        self.capture_directions = [DIRECTIONS["lu"], DIRECTIONS["ru"]] if color == "w" \
                                    else [DIRECTIONS["ld"], DIRECTIONS["rd"]]
        img_path = IMG_PATHS[color + "P"]
        super().__init__(pos, color, board, img_path)

    def _calculate_moves(self) -> Iterable[Position]:
        steps = [1, 2] if self.in_start_pos else [1]
        for dx, dy in self.directions:
            for step in steps:
                new_pos = Position(self.pos.file_idx + dx * step, self.pos.rank_idx + dy * step)

                if self.new_pos_possible(new_pos) == 1:
                    yield new_pos

        for dx, dy in self.capture_directions:
            new_pos = Position(self.pos.file_idx + dx, self.pos.rank_idx + dy)
            if self.can_capture(new_pos):
                yield new_pos