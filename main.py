import tkinter as tk
import tkinter.messagebox
from game.coord import *
from game.piece import *
from game.tier1 import *

# Create the main window and set its size
root = tk.Tk()
root.geometry("1100x1100")
root.title("Miankil")
root.configure(bg='black')

# Create a frame to hold the buttons
frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor='center')

# Create a label to display messages
message_label = tk.Label(root, text='', bg='lightblue', fg='red', font=('Arial', 12))
message_label.pack()

# Create a 11x11 grid of buttons with improved appearance
buttons = [[None for _ in range(11)] for _ in range(11)]
for i in range(11):
    for j in range(11):
        button_color = 'lightblue' if (i + j) % 2 == 0 else 'white'
        button = tk.Button(frame, text='', height=2, width=4, \
            bg=button_color, fg='red', font=('Arial', 11), bd=5, \
            relief='groove', command=lambda x=j, y=10-i: on_button_click(x, y))
        button.grid(row=i, column=j)
        buttons[i][j] = button

# Create a 11x11 list to hold the pieces
board = [[None for _ in range(11)] for _ in range(11)]

# Create a variable to hold the piece that is being moved
selected_piece = None
selected_coord = None

# Function to create a new piece on the board
def create_piece(piece, color, coord):
    board[coord.x][coord.y] = piece(color)

# Function to handle button clicks
def on_button_click(x, y):
    global selected_piece
    global selected_coord
    coord = Coord(x, y)
    if selected_piece:
        # If a piece is selected, move it to the clicked cell
        if is_valid_move(selected_piece, selected_coord, coord):
            board[coord.x][coord.y] = selected_piece
            selected_piece = None
            selected_coord = None
            message_label['text'] = ''  # Clear the message
    else:
        # If no piece is selected, check if there is a piece in the clicked cell
        if board[coord.x][coord.y] is None:
            # If there is no piece, display a message on the window
            message_label['text'] = f'{coord.x}, {coord.y} is empty'
        else:
            # If there is a piece, pick it up
            selected_piece = board[coord.x][coord.y]
            selected_coord = coord
            board[coord.x][coord.y] = None
            message_label['text'] = f'Having {selected_piece}'

    # Update the button text
    for i in range(11):
        for j in range(11):
            piece = board[i][j]
            buttons[i][j]['text'] = piece if piece else ''

def is_empty(board, x, y):
    return board[x][y] is None

def is_empty_line(board, start, end):
    # Check if the start and end coordinates are not on the same row
    if start.x != end.x and start.y != end.y:
        return False
    
    for i in range(start.x + 1, end.x):
        for j in range(start.y + 1, end.y):
            if not is_empty(board, i, j):
                return False

def is_empty_diagonal(board, start, end):
    # Check if the start and end coordinates are not on the same diagonal
    if abs(start.x - end.x) != abs(start.y - end.y):
        return False
    
    for i in range(start.x + 1, end.x):
        for j in range(start.y + 1, end.y):
            if not is_empty(board, i, j):
                return False

def is_valid_move(piece : Piece, start, end):
    try:
        return piece.can_move(start, end)
    except:
        return True

# Initialize the board with some pieces
create_piece(Pawn, 'white', Coord(0, 0))

# Start the Tkinter event loop
root.mainloop()