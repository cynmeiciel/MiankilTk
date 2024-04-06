import tkinter as tk
import tkinter.messagebox

from .board import *
from .coord import *
from .piece import *
from .tier0 import *
from .tier1 import *


class Game:
    def __init__(self):
        self.board = Board()
        self.successfully = False
        self.turn = Turn.BLUE
        self.selected_coord = None
        self.selected_piece = None
        self.dead_pieces = {Turn.RED: [], Turn.BLUE: []}
        
        self.init_tk()
        
        self.buttons = [[None for _ in range(11)] for _ in range(11)]
        for i in range(11):
            for j in range(11):
                button_color = 'deepskyblue4' if (i + j) % 2 == 0 else 'slategray1'
                button = tk.Button(self.frame, text='', height=3, width=6, \
                    bg=button_color, fg='red', font=('Arial', 11), bd=5, \
                    border=3, \
                    relief='groove', command=lambda x=j, y=i: self.on_button_click(x, y))
                button.grid(row=10-i, column=j+1)
                self.buttons[j][i] = button
    
    def init_tk(self):
        # Create the main window (fullscreen) and set its size
        self.root = tk.Tk()
        self.root.geometry('1600x960')
        self.root.title('Miankil')
        self.root.configure(bg='black')

        # Create a frame to hold the buttons
        self.frame = tk.Frame(self.root)
        self.frame.place(relx=0.5, rely=0.5, anchor='center')
        self.frame.configure(bg='lightblue')

        # Create a new frame that sticks to the right of the current frame
        right_frame = tk.Frame(self.root)
        right_frame.place(relx=1.0, rely=0.5, anchor='e')
        right_frame.configure(bg='cyan')

        # Or create a new frame that sticks to the left of the current frame
        left_frame = tk.Frame(self.root)
        left_frame.pack(side='left')
        left_frame.configure(bg='aqua')

        # Create a label to display messages
        self.labels = {
            'message': tk.Label(self.root, text='', bg='lightblue', fg='red', font=('Arial', 12)),
            # 'turn': tk.Label(self.root, text='', bg='lightblue', fg='red', font=('Arial', 12)),
            # 'dead_pieces': tk.Label(self.root, text='', bg='lightblue', fg='red', font=('Arial', 12))
        }
        for label in self.labels.values():
            label.pack()
        
        # Create labels for the coordinates
        for i in range(11):
            tk.Label(self.frame, text=str(i), bg='lightblue', fg='red', font=('Arial', 11)).grid(row=10-i, column=0)
            tk.Label(self.frame, text=str(i), bg='lightblue', fg='red', font=('Arial', 11)).grid(row=11, column=i+1)
    
    def on_button_click(self, x, y) -> None:
        coord = Coord(x, y)
        if self.selected_piece:
            # If a piece is selected, move it to the clicked cell
            if self.selected_piece.can_move(self.selected_coord, coord):
                # if dead:=self.board.board[coord.x][coord.y]:
                #     self.dead_pieces[self.turn].append(dead)
                self.board.board[coord.x][coord.y] = self.selected_piece
                self.board.board[self.selected_coord.x][self.selected_coord.y] = None
                self.labels['message']['text'] = f'Moved {self.selected_piece} to {coord.x}, {coord.y}'
            else:
                self.labels['message']['text'] = f'Invalid move for {self.selected_piece}'
            self.selected_coord = None
            self.selected_piece = None
            
        else:
            # self.labels['message']['text'] = 'cc'
            # If no piece is selected, check if there is a piece in the clicked cell
            if self.board.board[coord.x][coord.y] is None:
                # If there is no piece, display a message on the window
                self.labels['message']['text'] = f'{coord.x}, {coord.y} is empty'
            else:
                # If there is a piece, pick it up
                self.selected_piece = self.board.board[coord.x][coord.y]
                self.selected_coord = coord
                self.labels['message']['text'] = f'Having {self.selected_piece}'
                # self.labels['message']['text'] = 'ccx'

        # Update the button text
        for i in range(11):
            for j in range(11):
                piece = self.board.board[i][j]
                self.buttons[i][j]['text'] = piece if piece else ''
