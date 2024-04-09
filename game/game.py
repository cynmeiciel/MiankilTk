import tkinter as tk
import tkinter.messagebox
from tkinter import scrolledtext

from .board import *
from .coord import *
from .piece import *
from .tier0 import *
from .tier1 import *
from .tier2 import *
from .tier3 import *
from .tier4 import *


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
                button_bg = self.get_button_bg(i, j)
                button = tk.Button(self.frame, text='', height=3, width=6, \
                    bg=button_bg, fg='red', font=('Arial', 11), bd=5, \
                    border=3, \
                    relief='groove', command=lambda x=j, y=i: self.on_button_click(x, y))
                button.grid(row=10-i, column=j+1)
                button.bind('<Button-2>', lambda event, x=j, y=i: self.on_middle_click(x, y))
                button.bind('<Button-3>', lambda event, x=j, y=i: self.on_right_click(x, y))
                self.buttons[j][i] = button
        
        self.move_log = scrolledtext.ScrolledText(self.root, width=30, height=30, state='disabled', bg='lightblue', fg='crimson', font=('Consolas', 13))
        self.move_log.pack(side=tk.RIGHT)
                
        self.marked_cells = []
        self.posible_moves = []
        
        self.update_button()
        
        self.labels['message']['text'] = 'Welcome to Miankil!'
           
    def init_tk(self):
        # Create the main window (fullscreen) and set its size
        self.root = tk.Tk()
        self.fullscreen = False
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.minsize(800, 600)
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
            tk.Label(self.frame, text=str(i), bg='lightblue', fg='crimson', font=('Arial', 11)).grid(row=10-i, column=0)
            tk.Label(self.frame, text=str(i), bg='lightblue', fg='crimson', font=('Arial', 11)).grid(row=11, column=i+1)
    
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes('-fullscreen', self.fullscreen)
    
    def on_button_click(self, x, y) -> None:
        coord = Coord(x, y)
        if self.selected_piece:
            if self.board.find_piece(coord) is None or\
               self.board.find_piece(coord).is_blue != self.selected_piece.is_blue:
                self.handle_move(coord)
            else:
                self.handle_pick(coord)
        else:
            self.handle_pick(coord)
        
        self.update_button()
    
    def log_move(self, end):
        self.move_log.configure(state='normal')
        self.move_log.insert(tk.END, f'{self.selected_piece}{self.selected_coord} -> {end}\n')
        # self.move_log.see(tk.END)
        self.move_log.configure(state='disabled')
                
    def handle_move(self, coord) -> None:
        # If a piece is selected, move it to the clicked cell
        if self.selected_piece.can_move(self.selected_coord, coord):
            # if dead:=self.board.board[coord.x][coord.y]:
            #     self.dead_pieces[self.turn].append(dead)
            self.board.board[coord.x][coord.y] = self.selected_piece
            self.board.board[self.selected_coord.x][self.selected_coord.y] = None
            self.labels['message']['text'] = f'Moved {self.selected_piece} to {coord.x}, {coord.y}'
            self.log_move(coord)
        else:
            self.labels['message']['text'] = f'Invalid move for {self.selected_piece}'

        self.reset_button_bg(self.selected_coord)            
        self.selected_coord = None
        self.selected_piece = None
        
    
    def handle_pick(self, coord) -> None:
        # self.labels['message']['text'] = 'cc'
        # If no piece is selected, check if there is a piece in the clicked cell
        if self.board.board[coord.x][coord.y] is None:
            # If there is no piece, display a message on the window
            self.labels['message']['text'] = f'{coord.x}, {coord.y} is empty'
        elif self.selected_coord == coord:
            # If the same piece is clicked again, deselect it
            self.reset_button_bg(self.selected_coord)
            self.selected_coord = None
            self.selected_piece = None
            self.labels['message']['text'] = 'Deselected'
        else:
            # If there is a piece, pick it up
            self.selected_piece = self.board.board[coord.x][coord.y]
            self.reset_button_bg(self.selected_coord)
            self.selected_coord = coord
            self.labels['message']['text'] = f'Having {self.selected_piece}'
            # self.labels['message']['text'] = 'ccx'
    
    def on_right_click(self, x, y):
        self.labels['message']['text'] = f'Right click at {x}, {y}'
        
    def on_middle_click(self, x, y):
        self.set_button_bg(Coord(x, y), 'hotpink')
        self.marked_cells.append(Coord(x, y))
            
    def get_button_bg(self, x, y):
        return 'deepskyblue4' if (x + y) % 2 == 0 else 'slategray1'
    
    def set_button_bg(self, coord, color):
        if self.buttons[coord.x][coord.y] is not None:
            self.buttons[coord.x][coord.y].config(bg=color)
        
    def reset_button_bg(self, coord):
        if coord is None:
            return
        self.buttons[coord.x][coord.y].config(bg=self.get_button_bg(coord.x, coord.y))
        
    def reset_marked_bg(self):
        for coord in self.marked_cells:
            self.reset_button_bg(coord)
        self.marked_cells = []
    
    def update_button(self):
        for i in range(11):
            for j in range(11):
                piece = self.board.board[i][j]
                self.buttons[i][j]['text'] = piece if piece else ''
                self.buttons[i][j]['fg'] = 'navy' if piece and piece.is_blue else 'crimson'
        
        self.reset_highlight()
        
        if self.selected_coord:
            self.set_button_bg(self.selected_coord, 'aqua')
            self.posible_moves = self.selected_piece.get_moves(self.board, self.selected_coord)
            self.highlight_move()
        
        self.reset_marked_bg()
            
    def highlight_move(self):        
        for coord in self.posible_moves:
            self.set_button_bg(coord, 'SpringGreen2')
    
    def reset_highlight(self):
        for coord in self.posible_moves:
            self.reset_button_bg(coord)
            
        self.posible_moves = []