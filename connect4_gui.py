import tkinter as tk
from tkinter import messagebox
from connect4_logic import Connect4GameLogic, PLAYER, AI, COLS, ROWS

class Connect4GameGUI:
    def __init__(self, root):
        self.logic = Connect4GameLogic()
        self.root = root
        self.root.title("Connect 4 AI Game")

        self.canvas = tk.Canvas(root, width=COLS * 100, height=ROWS * 100, bg="blue")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)
        self.draw_board()

        self.control_frame = tk.Frame(root)
        self.control_frame.pack()

        self.depth_label = tk.Label(self.control_frame, text="Search Depth (K):")
        self.depth_label.pack(side=tk.LEFT)

        self.depth_slider = tk.Scale(self.control_frame, from_=1, to=10, orient=tk.HORIZONTAL, label="Depth")
        self.depth_slider.set(4)
        self.depth_slider.pack(side=tk.LEFT)

        self.alpha_beta_var = tk.BooleanVar(value=True)
        self.alpha_beta_checkbox = tk.Checkbutton(self.control_frame, text="Use Alpha-Beta", variable=self.alpha_beta_var)
        self.alpha_beta_checkbox.pack(side=tk.LEFT)

        self.reset_button = tk.Button(self.control_frame, text="Reset Game", command=self.reset_game)
        self.reset_button.pack(side=tk.LEFT)

        self.status_label = tk.Label(root, text="Your Turn", font=("Arial", 14))
        self.status_label.pack()

        self.game_over = False

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(ROWS):
            for col in range(COLS):
                x0 = col * 100 + 10
                y0 = row * 100 + 10
                x1 = x0 + 80
                y1 = y0 + 80
                color = "white"
                if self.logic.board[row][col] == PLAYER:
                    color = "red"
                elif self.logic.board[row][col] == AI:
                    color = "yellow"
                self.canvas.create_oval(x0, y0, x1, y1, fill=color, outline="black")

    def handle_click(self, event):
        if self.game_over:
            return  # Do nothing if game over

        col = event.x // 100
        if self.logic.is_valid_move(col):
            player_won = self.logic.make_move(col, PLAYER)
            self.draw_board()

            if player_won:
                self.show_winner("You Win!")
                return
            if self.logic.is_board_full():
                self.show_winner("It's a Tie!")
                return

            self.status_label.config(text="AI Thinking...")
            self.root.after(500, self.ai_move)
        else:
            messagebox.showwarning("Invalid Move", "This column is full! Try another one.")

    def ai_move(self):
        if self.game_over:
            return  # Do nothing if game over

        depth = self.depth_slider.get()
        self.logic.k = depth
        self.logic.use_alpha_beta = self.alpha_beta_var.get()

        _, col = self.logic.minimax(self.logic.board, self.logic.k, -float("inf"), float("inf"), True)

        if col is not None:
            ai_won = self.logic.make_move(col, AI)
            self.draw_board()

            if ai_won:
                self.show_winner("AI Wins!")
                return
            if self.logic.is_board_full():
                self.show_winner("It's a Tie!")
                return

        self.status_label.config(text="Your Turn")

    def show_winner(self, message):
        self.game_over = True
        self.status_label.config(text=message)
        messagebox.showinfo("Game Over", message)
        self.canvas.unbind("<Button-1>")  # Disable further clicks

    def reset_game(self):
        self.logic.reset_game()
        self.draw_board()
        self.status_label.config(text="Your Turn")
        self.canvas.bind("<Button-1>", self.handle_click)
        self.game_over = False

if __name__ == "__main__":
    root = tk.Tk()
    gui = Connect4GameGUI(root)
    root.mainloop()
