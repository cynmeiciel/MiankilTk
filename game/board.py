from .coord import *
from .piece import *
from .tier0 import *
from .tier1 import *

class Board:
    def __init__(self):
        self.board = [[None for _ in range(11)] for _ in range(11)]
        
        self.board[0][0] = Pawn(True)
        
        self.init_board()
    
    def init_buttons(self, buttons) -> None:
        self.buttons = buttons
        
    def init_board(self) -> None:
        pass
    
    def find_piece(self, coord : Coord) -> Piece:
        return self.board[coord.x][coord.y]
    
    def is_valid_move(self, piece, start : Coord, end : Coord) -> bool:
        if piece is None:
            return False
        return piece.can_move(self, start, end)
    
    def is_empty(self, coord : Coord) -> bool:
        return self.board[coord.x][coord.y] is None
    
    def is_empty_line(self, start, end) -> bool:
        # Check if the start and end coordinates are not on the same row
        if start.x != end.x and start.y != end.y:
            return False
        
        for i in range(start.x + 1, end.x):
            for j in range(start.y + 1, end.y):
                if not self.is_empty(i, j):
                    return False
        return True
    
    def is_empty_diagonal(self, start, end) -> bool:
        # Check if the start and end coordinates are not on the same diagonal
        if abs(start.x - end.x) != abs(start.y - end.y):
            return False
        
        for i in range(start.x + 1, end.x):
            for j in range(start.y + 1, end.y):
                if not self.is_empty(i, j):
                    return False
        return True
    
    def create_piece(self, piece, coord, is_blue=None) -> None:
        if is_blue is None:
            self.board[coord.x][coord.y] = piece
        else:
            self.board[coord.x][coord.y] = piece(is_blue)
        
    def reset_game(self) -> None:
        self.board = [[None for _ in range(11)] for _ in range(11)]
        
        self.init_board()


# Create a button to reset the game
# reset_button = tk.Button(right_frame, text='Reset', bg='red', fg='white', font=('Arial', 12), command=reset)
# reset_button.place(x=50, y=50)

# Create a 11x11 list to hold the pieces
# board = [[None for _ in range(11)] for _ in range(11)]


# Function to handle button clicks (mainloop)
# def on_button_click(x, y):
#     coord = Coord(x, y)
#     if selected_piece:
#         # If a piece is selected, move it to the clicked cell
#         if is_valid_move(selected_piece, selected_coord, coord):
#             board.board[coord.x][coord.y] = selected_piece
#             message_label['text'] = f'Moved {selected_piece} to {coord.x}, {coord.y}'
#             selected_piece = None
#             selected_coord = None
#     else:
#         # If no piece is selected, check if there is a piece in the clicked cell
#         if board[coord.x][coord.y] is None:
#             # If there is no piece, display a message on the window
#             message_label['text'] = f'{coord.x}, {coord.y} is empty'
#         else:
#             # If there is a piece, pick it up
#             selected_piece = board[coord.x][coord.y]
#             selected_coord = coord
#             board[coord.x][coord.y] = None
#             message_label['text'] = f'Having {selected_piece}'

#     # Update the button text
#     for i in range(11):
#         for j in range(11):
#             piece = board[i][j]
#             buttons[i][j]['text'] = piece if piece else ''
