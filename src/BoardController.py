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
        items = self.board.find_withtag("current")
        if not items or "piece" not in self.board.gettags(items[0]):
            return

        self.drag_item_id = items[0]
        self.piece = self.board.id_to_piece[self.drag_item_id]
        self.board.draw_possible_moves(self.piece)
        self.board.tag_raise(self.drag_item_id)

        x, y = self.board.coords(self.drag_item_id)
        self.offset_x = event.x - x
        self.offset_y = event.y - y


    def drag_piece(self, event):
        if not self.drag_item_id:
            return

        new_x = event.x - self.offset_x
        new_y = event.y - self.offset_y
        self.board.coords(self.drag_item_id, new_x, new_y)


    def place_piece(self, event):
        # calculate the idx of the square the piece was dropped on
        square_pos = calculate_position(event.x, event.y)

        if self.piece.can_move(square_pos):
            # calculate the canvas coords of the center of the square
            square_center_x, square_center_y = square_pos.calculate_board_coords()
            # move the piece visually to the new position
            self.board.coords(self.drag_item_id, square_center_x, square_center_y)
            # update the piece's position in the board'
            self.piece.move_to(square_pos)

        else:
            # snap back to original position
            self.board.coords(self.drag_item_id, *self.piece.pos.calculate_board_coords())

        self.board.clear_possible_moves()
        self.drag_item_id = None
