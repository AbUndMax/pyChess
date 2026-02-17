from chess.Pieces import *
from chess.Position import Position
import tkinter as tk
from Constants import FILE_SIZE, RANK_SIZE, SQUARE_PX, BOARD_FILE_PX, BOARD_RANK_PX
from BoardController import BoardController
from Dialog import GameOver


class Board(tk.Canvas):

    def __init__(self, master, restart_callback):
        super().__init__(
            master,
            width=BOARD_FILE_PX - 3,
            height=BOARD_RANK_PX - 3,
            # minus 3 because there are some weird additional pixels on bottom and right. -3 perfectly cuts them off
        )
        self.restart_callback = restart_callback
        self.pack()
        self.draw_board()

        # holds the graphical representation of each chess piece, mapping image ids to pieces
        self.id_to_piece: dict[int, Piece] = {}
        # holds the board state, mapping positions to pieces
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

        # Lists for storing captured pieces
        self.black_captured_pieces = []
        self.white_captured_pieces = []
        self.current_turn = "w"

        self.controller = BoardController(self)


    def draw_board(self):
        """
        Draws a chessboard-like grid pattern on the canvas.

        The method iterates over the grid's dimensions defined by constants FILE_SIZE
        and RANK_SIZE. It calculates the color for each square based on the parity of
        the sum of file and rank indices. Squares with an even parity are assigned
        a "white" color, while odd parity squares are assigned a dark color (hexadecimal
        value `#333333`). Each square is then drawn as a rectangle on the canvas.

        :return: None
        """
        for file_idx in range(FILE_SIZE):
            for rank_idx in range(RANK_SIZE):
                tile_color = "white" if (file_idx + rank_idx) % 2 == 0 else "#333333"
                self.create_rectangle(file_idx * SQUARE_PX,
                                      rank_idx * SQUARE_PX,
                                      (file_idx + 1) * SQUARE_PX,
                                      (rank_idx + 1) * SQUARE_PX,
                                      fill=tile_color)


    def draw_piece(self, piece: Piece) -> int:
        """
        Draws a chess piece on the game board at the position calculated from the piece's
        coordinates. The piece's image is created and associated with an identifier, which
        is stored for later reference.

        :param piece: The chess piece object to be drawn. It includes attributes like its
            position and image.
        :return: The identifier of the created image, which uniquely associates the drawn
            piece with its corresponding graphical element.
        """
        file_idx, rank_idx = piece.pos.calculate_board_coords()
        img_id = self.create_image(file_idx, rank_idx, image=piece.img, tags="piece")
        self.id_to_piece[img_id] = piece
        return img_id


    def draw_possible_moves(self, piece: Piece):
        """
        Draws possible moves for a given chess piece by visually representing them on the board
        with circular indicators.

        This method iterates over the moves calculated for the specified piece, determines the
        corresponding board coordinates for each move, and renders a visual circle at those positions
        indicating where the piece can move. The size and appearance of the circular indicators are
        predefined.

        :param piece: The chess piece for which the possible moves are to be displayed. This object
            contains the list of moves with their respective board coordinates.
        """
        for pos in piece.moves:
            x, y = pos.calculate_board_coords()
            for half_edge, color in zip([SQUARE_PX / 2 * 0.3, SQUARE_PX / 2 * 0.2], ["#73B2D9", "#C3DEEF"]):
                self.create_oval(x - half_edge,
                                 y - half_edge,
                                 (x + half_edge),
                                 (y + half_edge),
                                 fill=color,
                                 tags="possible_move",
                                 outline="")


    def clear_possible_moves(self):
        self.delete("possible_move")


    def is_free(self, pos: Position) -> bool:
        """
        Determine whether a specific position is free on the board.

        :param pos: The position to be checked for availability.
        :return: True if the position is free (not occupied by any piece), False otherwise.
        """
        return pos not in self.position_to_piece


    def pos_occupied_by(self, pos: Position) -> Piece:
        """
        Retrieves the chess piece situated at the given position on the board.

        This function takes a `Position` object as input and queries the
        internal mapping from positions to pieces to determine which chess
        piece, if any, currently occupies the specified position.

        :param pos: The `Position` object representing the location on the board
            to check for an occupying chess piece.
        :return: The `Piece` object occupying the specified position on the board,
            or `None` if no chess piece is located at the given position.
        """
        return self.position_to_piece.get(pos)

    def capture_piece(self, pos: Position):
        """
        Captures a piece located at the provided position on the board. The method handles the
        removal of the piece from the visual representation and updates both the internal board
        state and the list of captured pieces based on the color of the captured piece.

        :param pos: Position object representing the location of the piece to be captured
        :return: None
        """
        piece = self.pos_occupied_by(pos)

        # delete piece visually
        self.delete(piece.item_id_on_board)

        # add piece to the respective capture list
        self.white_captured_pieces.append(piece) if piece.color == "w" \
            else self.black_captured_pieces.append(piece)

        # delete piece from board
        del self.id_to_piece[piece.item_id_on_board]
        del self.position_to_piece[piece.pos]

        if isinstance(piece, King):
            GameOver(self.master, self.current_turn, self.restart_callback)