import os
import tkinter as tk
from tkinter import simpledialog, messagebox, font

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

class Player:
    def __init__(self):
        self.name = ""
        self.symbol = ""
        
    def choose_name(self):
        while True:
            name = simpledialog.askstring("Player Setup", "Enter your name (letters only):")
            if name.isalpha():
                self.name = name
                break
            messagebox.showerror("Invalid Input", "Invalid name, please use letters only")
    
    def choose_symbol(self):
        while True:
            symbol = simpledialog.askstring("Player Setup", f"{self.name}, choose your symbol (a single letter):")
            if symbol.isalpha() and len(symbol) == 1:
                self.symbol = symbol.upper()
                break
            messagebox.showerror("Invalid Input", "Invalid symbol, please use a single letter")
    
class Menu:
    def display_main_menu(self):
        choice = messagebox.askquestion("Main Menu", "Welcome to X/O\nDo you want to start the game?")
        return "1" if choice == "yes" else "2"
    
    def display_end_game(self):
        choice = messagebox.askquestion("Game Over", "Game Over!\nDo you want to restart the game?")
        return "1" if choice == "yes" else "2"

class Board:
    def __init__(self, root):
        self.board = [str(i) for i in range(1, 10)]
        self.buttons = []
        self.root = root
        self.create_board()
    
    def create_board(self):
        for i in range(9):
            button = tk.Button(self.root, text=self.board[i], width=10, height=3, command=lambda i=i: game.play_turn(i),
                               font=font.Font(family="Helvetica", size=24, weight="bold"), bg="black", fg="white", activebackground="gray")
            button.grid(row=i//3, column=i%3, sticky="nsew")
            self.buttons.append(button)
    
    def update_board(self, choice, symbol):
        if self.is_valid_move(choice):
            self.board[choice] = symbol
            self.buttons[choice].config(text=symbol, state="disabled")
            return True
        return False
    
    def is_valid_move(self, choice):
        return self.board[choice].isdigit()
                    
    def reset_board(self):
        self.board = [str(i) for i in range(1, 10)]
        for i, button in enumerate(self.buttons):
            button.config(text=self.board[i], state="normal")

class Game:
    def __init__(self, root):
        self.players = [Player(), Player()]
        self.board = Board(root)
        self.menu = Menu()
        self.current_player_index = 0
        self.setup_players()
    
    def start_game(self):
        choice = self.menu.display_main_menu()
        if choice == "1":
            self.play_game()
        else:
            self.quit_game()
    
    def setup_players(self):
        for number, player in enumerate(self.players, start=1):
            player.choose_name()
            player.choose_symbol()
        clear_screen()
    
    def play_game(self):
        self.board.reset_board()
    
    def play_turn(self, cell_choice):
        player = self.players[self.current_player_index]
        if self.board.update_board(cell_choice, player.symbol):
            if self.check_win():
                self.board.root.after(100, lambda: messagebox.showinfo("Game Over", f"Congratulations, {player.name}! You won!"))
                self.end_game()
            elif self.check_draw():
                self.board.root.after(100, lambda: messagebox.showinfo("Game Over", "It's a tie!"))
                self.end_game()
            else:
                self.switch_player()
    
    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index
    
    def end_game(self):
        choice = self.menu.display_end_game()
        if choice == "1":
            self.restart_game()
        else:
            self.quit_game()

    def restart_game(self):
        self.board.reset_board()
        self.current_player_index = 0
    
    def check_win(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]  # diagonals
        ]
        for combo in winning_combinations:
            if self.board.board[combo[0]] == self.board.board[combo[1]] == self.board.board[combo[2]]:
                return True
        return False
    
    def check_draw(self):
        return all(not cell.isdigit() for cell in self.board.board)
    
    def quit_game(self):
        messagebox.showinfo("Quit Game", "Thank you for playing!")
        self.board.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tic Tac Toe")
    
    # Set the window to be stretchable
    for i in range(3):
        root.grid_rowconfigure(i, weight=1)
        root.grid_columnconfigure(i, weight=1)
    
    # Set the background color of the window to black
    root.configure(bg="black")
    
    game = Game(root)
    game.start_game()
    root.mainloop()
