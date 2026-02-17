from chess.Board import Board
from Constants import BOARD_GEOMETRY
import tkinter as tk

def main():
    root = tk.Tk()

    board = None

    def start_new_game():
        nonlocal board
        if board is not None:
            board.destroy()
        board = Board(root, restart_callback=start_new_game)

    start_new_game()
    root.mainloop()



if __name__ == '__main__':
    main()
