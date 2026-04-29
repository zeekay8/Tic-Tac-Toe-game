"""
Tic Tac Toe Game with GUI
Built with Python and Tkinter
Two-player mode with win/draw detection and score tracking
"""

import tkinter as tk
from tkinter import messagebox


class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.resizable(False, False)
        
        # Game variables
        self.board = [["", "", ""] for _ in range(3)]
        self.current_player = "X"
        self.game_active = True
        self.player_x_score = 0
        self.player_o_score = 0
        
        # Colors
        self.colors = {
            "X": "#2196F3",      # Blue
            "O": "#FF5722",      # Orange
            "bg": "#1a1a2e",     # Dark background
            "btn_bg": "#16213e",  # Button background
            "text": "#eeeeee",    # Light text
            "hover": "#0f3460"    # Hover color
        }
        
        self.window.configure(bg=self.colors["bg"])
        
        # Create GUI elements
        self.create_score_display()
        self.create_board()
        self.create_control_buttons()
        
    def create_score_display(self):
        """Create the score display frame"""
        score_frame = tk.Frame(self.window, bg=self.colors["bg"])
        score_frame.pack(pady=10)
        
        self.x_score_label = tk.Label(
            score_frame, 
            text=f"Player X: {self.player_x_score}", 
            font=("Arial", 16, "bold"),
            fg=self.colors["X"],
            bg=self.colors["bg"]
        )
        self.x_score_label.pack(side=tk.LEFT, padx=20)
        
        self.o_score_label = tk.Label(
            score_frame, 
            text=f"Player O: {self.player_o_score}", 
            font=("Arial", 16, "bold"),
            fg=self.colors["O"],
            bg=self.colors["bg"]
        )
        self.o_score_label.pack(side=tk.RIGHT, padx=20)
        
        # Turn indicator
        self.turn_label = tk.Label(
            self.window,
            text="Player X's turn",
            font=("Arial", 14),
            fg=self.colors["text"],
            bg=self.colors["bg"]
        )
        self.turn_label.pack(pady=5)
    
    def create_board(self):
        """Create the 3x3 game board buttons"""
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        board_frame = tk.Frame(self.window, bg=self.colors["bg"])
        board_frame.pack(pady=10)
        
        for row in range(3):
            for col in range(3):
                button = tk.Button(
                    board_frame,
                    text="",
                    font=("Arial", 40, "bold"),
                    width=4,
                    height=2,
                    bg=self.colors["btn_bg"],
                    fg=self.colors["text"],
                    activebackground=self.colors["hover"],
                    relief=tk.RAISED,
                    borderwidth=2,
                    command=lambda r=row, c=col: self.make_move(r, c)
                )
                button.grid(row=row, column=col, padx=3, pady=3)
                
                # Add hover effect
                button.bind("<Enter>", lambda e, b=button: self.on_hover(b))
                button.bind("<Leave>", lambda e, b=button: self.on_leave(b))
                
                self.buttons[row][col] = button
    
    def create_control_buttons(self):
        """Create reset and quit buttons"""
        control_frame = tk.Frame(self.window, bg=self.colors["bg"])
        control_frame.pack(pady=10)
        
        reset_btn = tk.Button(
            control_frame,
            text="New Game",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5,
            command=self.reset_game
        )
        reset_btn.pack(side=tk.LEFT, padx=10)
        
        quit_btn = tk.Button(
            control_frame,
            text="Quit",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            padx=20,
            pady=5,
            command=self.window.quit
        )
        quit_btn.pack(side=tk.RIGHT, padx=10)
    
    def on_hover(self, button):
        """Handle mouse hover effect"""
        if button["text"] == "" and self.game_active:
            button["bg"] = self.colors["hover"]
    
    def on_leave(self, button):
        """Handle mouse leave effect"""
        if button["text"] == "":
            button["bg"] = self.colors["btn_bg"]
    
    def make_move(self, row, col):
        """Handle player move when a button is clicked"""
        if self.board[row][col] == "" and self.game_active:
            # Update board and button
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(
                text=self.current_player,
                fg=self.colors[self.current_player],
                bg=self.colors["btn_bg"]
            )
            
            # Check win or tie
            if self.check_win():
                winner = self.current_player
                self.game_active = False
                
                # Update score
                if winner == "X":
                    self.player_x_score += 1
                    self.x_score_label.config(text=f"Player X: {self.player_x_score}")
                else:
                    self.player_o_score += 1
                    self.o_score_label.config(text=f"Player O: {self.player_o_score}")
                
                # Highlight winning cells
                self.highlight_winner()
                
                messagebox.showinfo("Game Over", f"Player {winner} wins!")
                
            elif self.check_tie():
                self.game_active = False
                messagebox.showinfo("Game Over", "It's a tie!")
                
            else:
                # Switch players
                self.current_player = "O" if self.current_player == "X" else "X"
                self.turn_label.config(
                    text=f"Player {self.current_player}'s turn",
                    fg=self.colors[self.current_player]
                )
    
    def check_win(self):
        """Check if current player has won"""
        b = self.board
        # Check rows, columns and diagonals
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] == self.current_player:  # Row
                self.win_combo = [(i, 0), (i, 1), (i, 2)]
                return True
            if b[0][i] == b[1][i] == b[2][i] == self.current_player:  # Column
                self.win_combo = [(0, i), (1, i), (2, i)]
                return True
        
        if b[0][0] == b[1][1] == b[2][2] == self.current_player:  # Main diagonal
            self.win_combo = [(0, 0), (1, 1), (2, 2)]
            return True
        if b[0][2] == b[1][1] == b[2][0] == self.current_player:  # Anti-diagonal
            self.win_combo = [(0, 2), (1, 1), (2, 0)]
            return True
        
        return False
    
    def highlight_winner(self):
        """Highlight the winning cells in green"""
        for row, col in self.win_combo:
            self.buttons[row][col].config(bg="#4CAF50")
    
    def check_tie(self):
        """Check if the game is a tie (board is full with no winner)"""
        return all(self.board[row][col] != "" for row in range(3) for col in range(3))
    
    def reset_game(self):
        """Reset the game board for a new round"""
        self.board = [["", "", ""] for _ in range(3)]
        self.current_player = "X"
        self.game_active = True
        self.turn_label.config(text="Player X's turn", fg=self.colors["text"])
        
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(
                    text="",
                    bg=self.colors["btn_bg"],
                    fg=self.colors["text"]
                )
    
    def run(self):
        """Start the game"""
        self.window.mainloop()


if __name__ == "__main__":
    game = TicTacToe()
    game.run()