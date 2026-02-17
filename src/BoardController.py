from chess.Position import calculate_position


class BoardController:


    def __init__(self, board):
        self.board = board

        self.drag_item_id = None
        self.piece = None
        self.offset_x = 0
        self.offset_y = 0

        board.bind("<Button-1>", self.pick_piece)
        board.bind("<B1-Motion>", self.drag_piece)
        board.bind("<ButtonRelease-1>", self.place_piece)


    #TODO: implement "click piece, click destination" logic (without dragging)


    def pick_piece(self, event):
        """
        Handles the selection of a game piece on the board when triggered by
        an event, such as a mouse click. Identifies the piece based on its tag
        and raises it in the visual hierarchy to indicate it has been picked.
        Additionally, computes the offsets for smooth movement of the piece
        during dragging.

        :param event: Event that triggers the piece selection, typically a
            mouse-click event containing cursor coordinates (x, y).
        :return: None
        """
        items = self.board.find_withtag("current")
        if not items or "piece" not in self.board.gettags(items[0]):
            return

        self.drag_item_id = items[0]
        self.piece = self.board.id_to_piece[self.drag_item_id]

        # check if it's the current player's turn
        if self.piece.color != self.board.current_turn:
            self.drag_item_id = None
            self.piece = None
            return

        self.board.draw_possible_moves(self.piece)
        self.board.tag_raise(self.drag_item_id)

        x, y = self.board.coords(self.drag_item_id)
        self.offset_x = event.x - x
        self.offset_y = event.y - y


    def drag_piece(self, event):
        """
        Handles the event of dragging a piece on the board.

        This method updates the position of the currently dragged item
        based on the new coordinates provided by the event. It calculates
        the new position by adjusting the event's x and y coordinates with
        the stored offset. The board's coordinates are then updated to reflect
        the new position.

        :param event: The event object containing the updated x and y
                      coordinates for the dragged piece.
        :return: None
        """
        if not self.drag_item_id:
            return

        new_x = event.x - self.offset_x
        new_y = event.y - self.offset_y
        self.board.coords(self.drag_item_id, new_x, new_y)


    def place_piece(self, event):
        """
        Handles the logic for placing a piece onto the board after it is dragged and released.

        This method calculates the position on the board where the piece was dropped based on
        the event coordinates and determines if the move is valid. If valid, it updates the
        piece's visual and logical position on the board. Otherwise, the piece snaps back to
        its original position. Regardless of the outcome, potential moves are cleared from the
        visual representation.

        :param event: The event containing the position coordinates where the piece
            was dropped.
        :return: None
        """
        if not self.drag_item_id:
            return

        # calculate the idx of the square the piece was dropped on
        square_pos = calculate_position(event.x, event.y)

        if self.piece.can_move(square_pos):
            # calculate the canvas coords of the center of the square
            square_center_x, square_center_y = square_pos.calculate_board_coords()
            # move the piece visually to the new position
            self.board.coords(self.drag_item_id, square_center_x, square_center_y)
            # update the piece's position in the board'
            self.piece.move_to(square_pos)

            # update turn
            self.board.current_turn = "b" if self.board.current_turn == "w" else "w"

        else:
            # snap back to original position
            self.board.coords(self.drag_item_id, *self.piece.pos.calculate_board_coords())

        self.board.clear_possible_moves()
        self.drag_item_id = None
