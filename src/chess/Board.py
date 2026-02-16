from chess.Pieces import *
from chess.Position import Position
import tkinter as tk
from Constants import FILE_SIZE, RANK_SIZE, SQUARE_PX, BOARD_FILE_PX, BOARD_RANK_PX
from BoardController import BoardController


class Board(tk.Canvas):

    def __init__(self, master):
        super().__init__(
            master,
            width=BOARD_FILE_PX - 3,
            height=BOARD_RANK_PX - 3,
            # minus 3 because there are some weird additional pixels on bottom and right. -3 perfectly cuts them off
        )
        self.pack()
        self.draw_board()

        self.piece_at: dict[Position, Piece] = {
            Position(0, 0): Rook(Position(0, 0), "w", self),
            Position(1, 0): Knight(Position(1, 0), "w", self),
            Position(2, 0): Bishop(Position(2, 0), "w", self),
            Position(3, 0): Queen(Position(3, 0), "w", self),
            Position(4, 0): King(Position(4, 0), "w", self),
            Position(5, 0): Bishop(Position(5, 0), "w", self),
            Position(6, 0): Knight(Position(6, 0), "w", self),
            Position(7, 0): Rook(Position(7, 0), "w", self),
            Position(0, 1): Pawn(Position(0, 1), "w", self),
            Position(1, 1): Pawn(Position(1, 1), "w", self),
            Position(2, 1): Pawn(Position(2, 1), "w", self),
            Position(3, 1): Pawn(Position(3, 1), "w", self),
            Position(4, 1): Pawn(Position(4, 1), "w", self),
            Position(5, 1): Pawn(Position(5, 1), "w", self),
            Position(6, 1): Pawn(Position(6, 1), "w", self),
            Position(7, 1): Pawn(Position(7, 1), "w", self),

            Position(0, 7): Rook(Position(0, 7), "b", self),
            Position(1, 7): Knight(Position(1, 7), "b", self),
            Position(2, 7): Bishop(Position(2, 7), "b", self),
            Position(3, 7): Queen(Position(3, 7), "b", self),
            Position(4, 7): King(Position(4, 7), "b", self),
            Position(5, 7): Bishop(Position(5, 7), "b", self),
            Position(6, 7): Knight(Position(6, 7), "b", self),
            Position(7, 7): Rook(Position(7, 7), "b", self),
            Position(0, 6): Pawn(Position(0, 6), "b", self),
            Position(1, 6): Pawn(Position(1, 6), "b", self),
            Position(2, 6): Pawn(Position(2, 6), "b", self),
            Position(3, 6): Pawn(Position(3, 6), "b", self),
            Position(4, 6): Pawn(Position(4, 6), "b", self),
            Position(5, 6): Pawn(Position(5, 6), "b", self),
            Position(6, 6): Pawn(Position(6, 6), "b", self),
            Position(7, 6): Pawn(Position(7, 6), "b", self)
        }

        self.controller = BoardController(self)


    def draw_board(self):
        for file in range(FILE_SIZE):
            for rank in range(RANK_SIZE):
                tile_color = "white" if (file + rank) % 2 == 0 else "#333333"
                self.create_rectangle(
                    file * SQUARE_PX,
                    rank * SQUARE_PX,
                    (file + 1) * SQUARE_PX,
                    (rank + 1) * SQUARE_PX,
                    fill=tile_color
                )