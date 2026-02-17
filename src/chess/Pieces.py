from abc import ABC, abstractmethod

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
    def moves(self) -> list[Position]:
        return self._calculate_moves()


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
    def _calculate_moves(self) -> list[Position]:
        """yield candidate move for this piece in current position"""
        ...


    def _calculate_ray_moves(self, directions):
        """
        Calculates potential moves for a piece based on a set of directions.

        Given a set of directions represented as tuples of (dx, dy), this method iterates
        through each direction to calculate all possible positions a piece can move along
        the specified rays until blocked, out of bounds, or a capture is encountered.

        :param directions: A list of tuples representing the directions in which
                           the piece can move.
        :type directions: list[tuple[int, int]]
        :return: A list of Position objects representing all valid moves calculated
                 along the ray directions.
        :rtype: list[Position]
        """
        moves = []
        for dx, dy in directions:
            for step in range(1, max(FILE_SIZE, RANK_SIZE)):
                new_pos = Position(self.pos.file_idx + dx * step, self.pos.rank_idx + dy * step)

                possible_code = self.new_pos_possible(new_pos)
                match possible_code:
                    case 0: # blocked by own color / out of bounds
                        break
                    case 1: # free
                        moves.append(new_pos)
                    case 2: # capture
                        moves.append(new_pos)
                        break
        return moves


    def can_capture(self, pos_to_capture: Position) -> bool:
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

    def _calculate_moves(self):
        moves = []
        step = 1
        for dx, dy in self.directions:
            new_pos = Position(self.pos.file_idx + dx * step, self.pos.rank_idx + dy * step)

            if self.new_pos_possible(new_pos):
                moves.append(new_pos)

        return moves



class Queen(Piece):

    def __init__(self, pos: Position, color: str, board):
        self.directions = [DIRECTIONS[d] for d in ["l", "r", "u", "d", "lu", "ru", "ld", "rd"]]
        img_path = IMG_PATHS[color + "Q"]
        super().__init__(pos, color, board, img_path)

    def _calculate_moves(self):
        return self._calculate_ray_moves(self.directions)




class Bishop(Piece):

    def __init__(self, pos: Position, color: str, board):
        self.directions = [DIRECTIONS[d] for d in ["lu", "ru", "ld", "rd"]]
        img_path = IMG_PATHS[color + "B"]
        super().__init__(pos, color, board, img_path)

    def _calculate_moves(self):
        return self._calculate_ray_moves(self.directions)



class Knight(Piece):

    def __init__(self, pos: Position, color: str, board):
        self.directions = [DIRECTIONS[d] for d in ["l", "r", "u", "d"]]
        img_path = IMG_PATHS[color + "N"]
        super().__init__(pos, color, board, img_path)

    def _calculate_moves(self):
        moves = []
        step = 2
        for dx, dy in self.directions:
            for i in (1, -1):
                new_pos = Position(self.pos.file_idx + dx * step + i * dy, self.pos.rank_idx + dy * step + i * dx)
                if self.new_pos_possible(new_pos):
                    moves.append(new_pos)

        return moves



class Rook(Piece):

    def __init__(self, pos: Position, color: str, board):
        self.directions = [DIRECTIONS[d] for d in ["l", "r", "u", "d"]]
        img_path = IMG_PATHS[color + "R"]
        super().__init__(pos, color, board, img_path)

    def _calculate_moves(self) -> list[Position]:
        return self._calculate_ray_moves(self.directions)



class Pawn(Piece):

    def __init__(self, pos: Position, color: str, board):
        self.directions = [DIRECTIONS["u"]] if color == "w" else [DIRECTIONS["d"]]
        self.capture_directions = [DIRECTIONS["lu"], DIRECTIONS["ru"]] if color == "w" \
                                    else [DIRECTIONS["ld"], DIRECTIONS["rd"]]
        img_path = IMG_PATHS[color + "P"]
        super().__init__(pos, color, board, img_path)

    def _calculate_moves(self) -> list[Position]:
        #TODO conditional steps since pawns can only clash sideways
        moves = []
        steps = [1, 2] if self.in_start_pos else [1]
        for dx, dy in self.directions:
            for step in steps:
                new_pos = Position(self.pos.file_idx + dx * step, self.pos.rank_idx + dy * step)

                if self.new_pos_possible(new_pos) == 1:
                    moves.append(new_pos)

        for dx, dy in self.capture_directions:
            new_pos = Position(self.pos.file_idx + dx, self.pos.rank_idx + dy)
            if self.can_capture(new_pos):
                moves.append(new_pos)

        return moves