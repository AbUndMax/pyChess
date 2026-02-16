from chess.Position import calculate_position


class BoardController:


    def __init__(self, board):
        self.board = board
        self.drag_item = None
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

        self.drag_item = items[0]

        x, y = self.board.coords(self.drag_item)
        self.offset_x = event.x - x
        self.offset_y = event.y - y


    def drag_piece(self, event):
        if not self.drag_item:
            return

        new_x = event.x - self.offset_x
        new_y = event.y - self.offset_y
        self.board.coords(self.drag_item, new_x, new_y)


    def place_piece(self, event):
        square_pos = calculate_position(event.x, event.y)
        square_center_x, square_center_y = square_pos.calculate_board_coords()
        self.board.coords(self.drag_item, square_center_x, square_center_y)
        self.drag_item = None
