import tkinter as tk
from Constants import FILE_SIZE, RANK_SIZE, SQUARE_PX, BOARD_FILE_PX, BOARD_RANK_PX

class ChessView(tk.Frame):


    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.canvas = tk.Canvas(self, width=BOARD_FILE_PX - 3, height=BOARD_RANK_PX - 3)
        # minus 3 because there are some weird additional pixels on bottom and right. -3 perfectly cuts them off
        self.canvas.pack()

        self.draw_board()


