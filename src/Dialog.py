import tkinter as tk


class GameOver(tk.Toplevel):


    def __init__(self, parent, winner_color: str, restart_callback):
        super().__init__(parent)
        self.parent = parent
        self.restart_callback = restart_callback
        self.title("Game Over")
        self.geometry("300x150")
        self.resizable(False, False)

        # Make dialog modal
        self.transient(parent)
        self.grab_set()

        # Center dialog over parent
        parent.update_idletasks()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()

        dialog_w = 300
        dialog_h = 150

        x = parent_x + (parent_w // 2) - (dialog_w // 2)
        y = parent_y + (parent_h // 2) - (dialog_h // 2)

        self.geometry(f"{dialog_w}x{dialog_h}+{x}+{y}")

        winner_text = "White wins!" if winner_color == "w" else "Black wins!"

        tk.Label(self, text=winner_text, font=("Arial", 16)).pack(pady=20)
        tk.Button(self, text="OK", command=self.on_restart).pack()


        self.wait_window()


    def on_restart(self):
        self.destroy()
        self.parent.after_idle(self.restart_callback)

