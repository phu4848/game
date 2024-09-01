import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")

        self.grid_size = 10
        self.num_mines = 10
        self.buttons = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.mines = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.revealed = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.flags = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.game_over = False

        self.create_widgets()
        self.place_mines()

    def create_widgets(self):
        self.restart_button = tk.Button(self.root, text="Start New Game", command=self.restart_game)
        self.restart_button.grid(row=self.grid_size, column=0, columnspan=self.grid_size)

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                button = tk.Button(self.root, width=4, height=2, command=lambda r=row, c=col: self.on_button_click(r, c))
                button.bind('<Button-3>', lambda e, r=row, c=col: self.toggle_flag(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def place_mines(self):
        placed_mines = 0
        while placed_mines < self.num_mines:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            if not self.mines[row][col]:
                self.mines[row][col] = True
                placed_mines += 1

    def on_button_click(self, row, col):
        if self.game_over:
            return
        if self.flags[row][col]:
            return
        if self.mines[row][col]:
            self.reveal_mines()
            messagebox.showinfo("Game Over", "You clicked on a mine!")
            self.game_over = True
            return
        self.reveal_cell(row, col)
        if self.check_win():
            messagebox.showinfo("Congratulations", "You won the game!")
            self.game_over = True

    def reveal_cell(self, row, col):
        if self.revealed[row][col]:
            return
        self.revealed[row][col] = True
        num_adjacent_mines = self.count_adjacent_mines(row, col)
        button = self.buttons[row][col]
        if num_adjacent_mines > 0:
            button.config(text=str(num_adjacent_mines))
        else:
            button.config(text="")
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < self.grid_size and 0 <= c < self.grid_size:
                        self.reveal_cell(r, c)

    def count_adjacent_mines(self, row, col):
        count = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < self.grid_size and 0 <= c < self.grid_size and self.mines[r][c]:
                    count += 1
        return count

    def toggle_flag(self, row, col):
        if self.game_over or self.revealed[row][col]:
            return
        button = self.buttons[row][col]
        if self.flags[row][col]:
            button.config(text="")
            self.flags[row][col] = False
        else:
            button.config(text="F")
            self.flags[row][col] = True

    def reveal_mines(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.mines[row][col]:
                    self.buttons[row][col].config(text="M", bg="red")

    def check_win(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if not self.mines[row][col] and not self.revealed[row][col]:
                    return False
        return True

    def restart_game(self):
        self.game_over = False
        self.mines = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.revealed = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.flags = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.place_mines()
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.buttons[row][col].config(text="", bg="SystemButtonFace")

if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()


