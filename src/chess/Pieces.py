from abc import ABC, abstractmethod
from typing import Iterator
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
        self.color: str = color
        self.img = tk.PhotoImage(file=img_path)
        self.img_id = self.draw_piece(self.img)
        self.moves: list[Position] = self._possible_moves()


    def _possible_moves(self) -> list[Position]:
        """
        Calculate all possible positions this piece can move to.
        :return: A list of all possible positions this Piece can move to.
        """
        moves = []
        for pos in self._calculate_moves():
            if pos.in_bounds(): # TODO: add check for piece occupancy
                moves.append(pos)
        return moves


    def move_to(self, pos: Position) -> bool:
        """
        movie this piece to pos if pos is a valid move
        :param pos: position to move to
        :return: True if move is valid, False otherwise
        """
        if pos in self.moves:
            self.pos = pos
            self.moves = self._possible_moves()
            return True
        return False


    @abstractmethod
    def _calculate_moves(self) -> Iterator[Position]:
        """yield candidate move for this piece in current position"""
        ...


    def draw_piece(self, img):
        file_idx, rank_idx = self.pos.calculate_board_coords()
        return self.board.create_image(file_idx, rank_idx, image=img, tags="piece")




class King(Piece):

    def __init__(self, pos: Position, color: str, board):
        self.directions = [DIRECTIONS[d] for d in ["l", "r", "u", "d", "lu", "ru", "ld", "rd"]]
        img_path = IMG_PATHS[color + "K"]
        super().__init__(pos, color, board, img_path)

    def _calculate_moves(self):
        step = 1
        for dx, dy in self.directions:
            yield Position(self.pos.file_idx + dx * step, self.pos.rank_idx + dy * step)



class Queen(Piece):

    def __init__(self, pos: Position, color: str, board):
        self.directions = [DIRECTIONS[d] for d in ["l", "r", "u", "d", "lu", "ru", "ld", "rd"]]
        img_path = IMG_PATHS[color + "Q"]
        super().__init__(pos, color, board, img_path)

    def _calculate_moves(self):
        for step in range(0, max(FILE_SIZE, RANK_SIZE)):
            for dx, dy in self.directions:
                yield Position(self.pos.file_idx + dx * step, self.pos.rank_idx + dy * step)



class Bishop(Piece):

    def __init__(self, pos: Position, color: str, board):
        self.directions = [DIRECTIONS[d] for d in ["lu", "ru", "ld", "rd"]]
        img_path = IMG_PATHS[color + "B"]
        super().__init__(pos, color, board, img_path)

    def _calculate_moves(self):
        step = max(FILE_SIZE, RANK_SIZE)
        for dx, dy in self.directions:
            yield Position(self.pos.file_idx + dx * step, self.pos.rank_idx + dy)



class Knight(Piece):

    def __init__(self, pos: Position, color: str, board):
        self.directions = [DIRECTIONS[d] for d in ["l", "r", "u", "d"]]
        img_path = IMG_PATHS[color + "N"]
        super().__init__(pos, color, board, img_path)

    def _calculate_moves(self):
        step = 2
        for dx, dy in self.directions:
            for i in (1, -1):
                yield Position(self.pos.file_idx + dx * step + i * dy, self.pos.rank_idx + dy * step + i * dx)



class Rook(Piece):

    def __init__(self, pos: Position, color: str, board):
        self.directions = [DIRECTIONS[d] for d in ["l", "r", "u", "d"]]
        img_path = IMG_PATHS[color + "R"]
        super().__init__(pos, color, board, img_path)

    def _calculate_moves(self) -> Iterator[Position]:
        for step in range(0, max(FILE_SIZE, RANK_SIZE)):
            for dx, dy in self.directions:
                yield Position(self.pos.file_idx + dx * step, self.pos.rank_idx + dy * step)



class Pawn(Piece):

    def __init__(self, pos: Position, color: str, board):
        self.directions = [DIRECTIONS[d] for d in ["u", "lu", "ru"]]
        img_path = IMG_PATHS[color + "P"]
        super().__init__(pos, color, board, img_path)

    def _calculate_moves(self) -> Iterator[Position]:
        #TODO conditional steps since pawns can only clash sideways
        steps = [1, 2] if self.pos.rank_idx == 1 else [1]
        for step in steps:
            for dx, dy in self.directions:
                yield Position(self.pos.file_idx + dx * step, self.pos.rank_idx + dy * step)