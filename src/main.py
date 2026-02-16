from chess.Board import Board
from Constants import BOARD_GEOMETRY
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("pyChess")
    root.geometry(BOARD_GEOMETRY)
    Board(root)
    root.mainloop()


if __name__ == '__main__':
    main()
