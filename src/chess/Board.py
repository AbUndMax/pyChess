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

        self.id_to_piece: dict[int, Piece] = {}
        self.position_to_piece: dict[Position, Piece] = {
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
        for file_idx in range(FILE_SIZE):
            for rank_idx in range(RANK_SIZE):
                tile_color = "white" if (file_idx + rank_idx) % 2 == 0 else "#333333"
                self.create_rectangle(file_idx * SQUARE_PX,
                                      rank_idx * SQUARE_PX,
                                      (file_idx + 1) * SQUARE_PX,
                                      (rank_idx + 1) * SQUARE_PX,
                                      fill=tile_color)


    def draw_piece(self, piece: Piece):
        file_idx, rank_idx = piece.pos.calculate_board_coords()
        img_id = self.create_image(file_idx, rank_idx, image=piece.img, tags="piece")
        self.id_to_piece[img_id] = piece
        return img_id


    def draw_possible_moves(self, piece: Piece):
        for pos in piece.moves:
            x, y = pos.calculate_board_coords()
            for half_edge in [SQUARE_PX / 2 * 0.3, SQUARE_PX / 2 * 0.2]:
                self.create_oval(x - half_edge,
                                 y - half_edge,
                                 (x + half_edge),
                                 (y + half_edge),
                                 fill="#0010bb",
                                 tags="possible_move")


    def clear_possible_moves(self):
        self.delete("possible_move")