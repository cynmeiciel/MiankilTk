import tkinter as tk
import tkinter.messagebox as msgbox
import tkinter.simpledialog as smpldlg
from tkinter import scrolledtext
from tkinter import PhotoImage as PhImg
from tkinter import Canvas as Cvs
from PIL import Image, ImageTk

import winsound as ws

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
        
        self.init_tk()
        self.init_bind()
        self.init_images()
        
        # Initialize the main board with buttons
        self.buttons = [[None for _ in range(11)] for _ in range(11)]
        button_size = 70
        
        for i in range(11):
            for j in range(11):
                bg = SQUARE_COLORS[j][i]
                button = tk.Button(self.frame, text='', \
                    bg=bg, fg='red', font=('Bahnschrift', 11), bd=5, \
                    border=3, \
                    relief='groove', command=lambda x=j, y=i: self.on_button_click(x, y))
                button.grid(row=10-i, column=j+1, sticky='nsew')
                button.bind('<Button-2>', lambda event, x=j, y=i: self.on_middle_click(x, y))
                button.bind('<Button-3>', lambda event, x=j, y=i: self.on_right_click(x, y))
                self.buttons[j][i] = button
        
        for i in range(11):
            self.frame.grid_columnconfigure(i+1, minsize=button_size)
            self.frame.grid_rowconfigure(i, minsize=button_size)
        ###
        
        self.move_log = scrolledtext.ScrolledText(self.right_frame, width=30, height=30, state='disabled', bg='lavender', font=('Consolas', 13))
        self.move_log.pack(side=tk.RIGHT)
                
        self.marked_cells = []
        self.posible_moves = []
        
        self.reset_params()
        self.update_button()
        
        self.init_extra_button()
        
        self.labels['message']['text'] = 'Welcome to Miankil!'
           
           
    def init_tk(self) -> None:
        # Create the main window (fullscreen) and set its size
        self.root = tk.Tk()
        self.fullscreen = False
        self.root.title('Miankil')
        self.root.configure(bg='black')
        
        # Set the background image
        self.bg_image = PhImg(file='game/images/bg/cyn.png')
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a frame to hold the buttons
        self.frame = tk.Frame(self.root)
        self.frame.place(relx=0.48, rely=0.5, anchor='center')
        self.frame.configure(bg='lightblue')

        # Create a new frame that sticks to the right of the current frame
        self.right_frame = tk.Frame(self.root)
        self.right_frame.place(relx=1.0, rely=0.5, anchor='e')
        self.right_frame.configure(bg='cyan')
        
        # Create a new frame that sticks to the bottom-right of the current frame
        self.botrig_frame = tk.Frame(self.root)
        self.botrig_frame.place(relx=1.0, rely=1.0, anchor='se')
        self.botrig_frame.configure(bg='lightblue')
        
        # Create a new frame that sticks to the top-right of the current frame
        self.toprig_frame = tk.Frame(self.root)
        self.toprig_frame.place(relx=1.0, rely=0.0, anchor='ne')
        self.toprig_frame.configure(bg='lightblue')

        # Create a new frame that sticks to the left of the current frame
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side='left')
        self.left_frame.configure(bg='aqua')

        # Create a label to display messages
        self.labels = {
            'message': tk.Label(self.root, text='', bg='lavender', fg='dark slate gray', font=('Bahnschrift', 13, 'bold')),
            # 'turn': tk.Label(self.root, text='', bg='lightblue', fg='red', font=('Bahnschrift', 12)),
            # 'dead_pieces': tk.Label(self.root, text='', bg='lightblue', fg='red', font=('Bahnschrift', 12))
        }
        for label in self.labels.values():
            label.pack()
        
        # Create labels for the coordinates
        for i in range(11):
            tk.Label(self.frame, text=str(i), bg='lightblue', fg='crimson', font=('Bahnschrift', 11)).grid(row=10-i, column=0)
            tk.Label(self.frame, text=str(i), bg='lightblue', fg='crimson', font=('Bahnschrift', 11)).grid(row=11, column=i+1)
    
    
    def init_bind(self) -> None:
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<F5>', lambda event: self.restart())
        self.root.bind('<Escape>', lambda event: self.root.quit())
        self.root.bind('<grave>', lambda event: self.console())
        self.root.bind('<x>', lambda event: self.pending_delete())
    
    
    def init_pieces_button(self) -> None:
        def init(text, cmmd):
            bttn = tk.Button(self.botrig_frame, bg='lightblue', fg='red', font=('Bahnschrift', 8), \
                 command=cmmd)
            try:
                image = self.piece_IMG['blue'][text.lower()]
                bttn.config(image=image, compound='center')
            except KeyError:
                bttn['text'] = text
                
            return bttn
        
        self.piece_buttons : list[dict[str, tk.Button]] = []
        
        self.piece_buttons.append({
            'Nexus' : init('Nexus', lambda: self.on_pick_piece(Nexus)),
            'Custodian' : init('Custodian', lambda: self.on_pick_piece(Custodian))
        })
        self.piece_buttons.append({
            'Pawn' : init('Pawn', lambda: self.on_pick_piece(Pawn)),
            'Sentinel' : init('Sentinel', lambda: self.on_pick_piece(Sentinel)),
            'Scout' : init('Scout', lambda: self.on_pick_piece(Scout)),
            'Watcher' : init('Watcher', lambda: self.on_pick_piece(Watcher)),
            'Guard' : init('Guard', lambda: self.on_pick_piece(Guard))
        }
        )
        
        for button in self.piece_buttons[1].values():
            button.pack(fill=tk.BOTH, expand=1, side=tk.LEFT)
    
    
    def init_extra_button(self) -> None:
        init = lambda text, cmmd: tk.Button(self.right_frame, text=text, bg='lightblue', fg='red', font=('Bahnschrift', 11), width=6, height=1, command=cmmd)
        
        self.restart_button = init('🔄', self.restart)
        self.restart_button.pack(side=tk.TOP)
        self.fullscreen_button = init('⇱', self.toggle_fullscreen)
        self.fullscreen_button.pack(side=tk.TOP)
        self.quit_button = init('❌', self.root.quit)
        self.quit_button.pack(side=tk.TOP)
        self.console_button = init('🔧', self.console)
        self.console_button.pack(side=tk.TOP)
        self.delete_piece_button = init('x', self.pending_delete)
        self.delete_piece_button.pack(side=tk.TOP)
        
        self.init_pieces_button()
    
    
    def init_images(self) -> None:
        self.piece_IMG : dict[str, dict[str, PhImg]] = {
            'blue' : {
                'pawn' : PhImg(file='game/images/piece/blue_pawn.png'),
                # 'sentinel' : PhImg(file='game/images/piece/blue_sentinel.png'),
                # 'scout' : PhImg(file='game/images/piece/blue_scout.png'),
                # 'watcher' : PhImg(file='game/images/piece/blue_watcher.png'),
                'guard' : PhImg(file='game/images/piece/blue_guard.png'),
                'nexus' : PhImg(file='game/images/piece/blue_nexus.png')
            },
            'red' : {
                'pawn' : PhImg(file='game/images/piece/red_pawn.png'),
                # 'sentinel' : PhImg(file='game/images/piece/red_sentinel.png'),
                # 'scout' : PhImg(file='game/images/piece/red_scout.png'),
                # 'watcher' : PhImg(file='game/images/piece/red_watcher.png'),
                'guard' : PhImg(file='game/images/piece/red_guard.png'),
                'nexus' : PhImg(file='game/images/piece/red_nexus.png')
            }
        }
        
        # Resize the images
        for color in self.piece_IMG:
            for name in self.piece_IMG[color]:
                self.piece_IMG[color][name] = self.piece_IMG[color][name].subsample(12)
                if color == 'red':
                    # Convert the PhotoImage to a PIL Image
                    pil_image = ImageTk.getimage(self.piece_IMG[color][name])
                    # Flip the PIL Image
                    flipped_image = pil_image.transpose(Image.FLIP_TOP_BOTTOM)
                    # Convert the PIL Image back to a PhotoImage
                    self.piece_IMG[color][name] = ImageTk.PhotoImage(flipped_image)
    
    
    def toggle_fullscreen(self, event=None) -> None:
        self.fullscreen = not self.fullscreen
        self.root.attributes('-fullscreen', self.fullscreen)
    
    
    def toggle_dev_mode(self) -> None:
        self.dev_mode = not self.dev_mode
        self.labels['message']['text'] = 'Dev mode enabled' if self.dev_mode else 'Dev mode disabled'
    
    
    def console(self) -> None:
        command = smpldlg.askstring('Console', 'Enter command:')
        if command == 'restart':
            self.restart()
        elif command == 'quit':
            self.root.quit()
        elif command == 'toggle_fullscreen':
            self.toggle_fullscreen()
        elif command == 'dev_mode':
            self.toggle_dev_mode()
        
    def pending_delete(self) -> None:
        self.delete_pending = not self.delete_pending
        self.labels['message']['text'] = 'Delete pending' if self.delete_pending else 'Delete off'
    
    
    # END OF TKINTER INITIALIZATION
    # GAME LOGIC FUNCTIONS ON RUNTIME
    
           
    def log_move(self, end, drop: bool = False) -> None:
        # Log the move in the ScrolledText widget
        if drop:
            move_text = f'{self.selected_piece} dropped at {end}\n'
            side = 'blue' if self.turn else 'red'
            self.move_log.configure(state='normal')  # Enable editing
            self.move_log.insert(tk.END, move_text, side)
            self.move_log.configure(state='disabled')  # Disable editing
        else:
            move_text = f'{self.selected_piece}{self.selected_coord} -> {end}\n'
            side = 'blue' if self.selected_piece.is_blue else 'red'
            self.move_log.configure(state='normal')  # Enable editing
            self.move_log.insert(tk.END, move_text, side)
            self.move_log.configure(state='disabled')  # Disable editing

        # Configure the tag to use the appropriate color
        if self.selected_piece.is_blue:
            self.move_log.tag_config('blue', foreground='navy')
        else:
            self.move_log.tag_config('red', foreground='crimson')
           
           
    def handle_move(self, coord) -> None:
        # If a piece is selected, move it to the clicked cell
        if self.selected_piece.can_move(self.board, self.selected_coord, coord):
            self.board.move_piece(self.selected_coord, coord)
            self.labels['message']['text'] = f'Moved {self.selected_piece} to {coord.x}, {coord.y}'
            self.log_move(coord)
            self.turn = not self.turn
            ws.PlaySound('game/sfx/move.wav', ws.SND_FILENAME | ws.SND_ASYNC | ws.SND_NODEFAULT) 
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
            if self.board.board[coord.x][coord.y].is_blue == bool(self.turn):
                self.selected_piece = self.board.board[coord.x][coord.y]
                self.reset_button_bg(self.selected_coord)
                self.selected_coord = coord
                self.labels['message']['text'] = f'Having {self.selected_piece}'
            else:
                self.labels['message']['text'] = 'This is not your piece'
            # self.labels['message']['text'] = 'ccx'
    
    
    def handle_drop(self, coord) -> None:
        if self.board.find_piece(coord) is None:
            self.board.board[coord.x][coord.y] = self.selected_piece
            self.labels['message']['text'] = f'Dropped {self.selected_piece} at {coord.x}, {coord.y}'
            self.log_move(coord, drop=True)
            self.turn = not self.turn
            ws.PlaySound('game/sfx/move.wav', ws.SND_FILENAME | ws.SND_ASYNC | ws.SND_NODEFAULT)
        else:
            self.board.on_hand_pieces.append(self.selected_piece, self.turn)
        
        # self.reset_button_bg(None, )
        self.selected_coord = None
        self.selected_piece = None
    
    def on_button_click(self, x, y) -> None:
        coord = Coord(x, y)
        if (not self.selected_coord) and (self.selected_piece):
            self.handle_drop(coord)
        
        elif self.delete_pending:
            self.board.delete_piece(coord)
            self.delete_pending = False
            self.labels['message']['text'] = f'Deleted piece at {coord.x}, {coord.y}'
        
        elif not self.dev_mode:
            if self.selected_piece:
                if self.board.find_piece(coord) is None or\
                self.board.find_piece(coord).is_blue != self.selected_piece.is_blue:
                    self.handle_move(coord)
                else:
                    self.handle_pick(coord)
            else:
                self.handle_pick(coord)
                
        else: # Dev mode
            if self.selected_piece:
                if self.selected_coord == coord:
                    self.reset_button_bg(self.selected_coord)
                    self.selected_coord = None
                    self.selected_piece = None
                    self.labels['message']['text'] = 'Deselected'
                else:
                    self.board.move_piece(self.selected_coord, coord)
                    self.reset_button_bg(self.selected_coord)
                    self.selected_piece = None
                    self.selected_coord = None
            else:
                if self.board.find_piece(coord):
                    self.selected_piece = self.board.find_piece(coord)
                    self.selected_coord = coord 
            self.reset_highlight()
        
        self.update_button()
    
    
    def on_right_click(self, x, y) -> None:
        self.labels['message']['text'] = f'Right click at {x}, {y}'
        
        
    def on_middle_click(self, x, y) -> None:
        if (crd:=Coord(x, y)) in self.marked_cells:
            self.reset_button_bg(crd)
            self.marked_cells.remove(crd)
        else:    
            self.set_button_bg(crd, 'hotpink')
            self.marked_cells.append(crd)
            
    
    def on_pick_piece(self, piece : type) -> None:
        if self.dev_mode or self.board.on_hand_pieces.get(piece, self.turn):
            self.selected_piece = self.board.on_hand_pieces.get(piece, self.turn)
            self.labels['message']['text'] = f'Having {self.selected_piece}'
        
        self.update_button()
            
    def get_button_bg(self, x, y) -> str:
        return SQUARE_COLORS[x][y]
    
    def set_button_bg(self, coord, color) -> None:
        if self.buttons[coord.x][coord.y] is not None:
            self.buttons[coord.x][coord.y].config(bg=color)
        
        
    def reset_button_bg(self, coord) -> None:
        try:
            self.buttons[coord.x][coord.y].config(bg=self.get_button_bg(coord.x, coord.y))
        except AttributeError:
            pass
        
    def reset_marked_bg(self) -> None:
        for coord in self.marked_cells:
            self.reset_button_bg(coord)
        self.marked_cells = []
    
    
    def update_button(self) -> None:
        for i in range(11):
            for j in range(11):
                piece = self.board.board[i][j]
                if piece:
                    try:
                        image = self.piece_IMG['blue' if piece.is_blue else 'red'][piece.name.lower()]
                        self.buttons[i][j].config(image=image, compound='center')
                    except KeyError:
                        self.buttons[i][j]['text'] = piece
                        self.buttons[i][j]['fg'] = 'navy' if piece.is_blue else 'crimson'

                else:
                    self.buttons[i][j]['text'] = ''
                    self.buttons[i][j]['image'] = ''
                            
        self.reset_highlight()
        
        if self.selected_coord:
            self.set_button_bg(self.selected_coord, 'aqua')
            self.posible_moves = self.selected_piece.get_moves(self.board, self.selected_coord)
            self.highlight_move()
        
        self.reset_marked_bg()
           
            
    def highlight_move(self) -> None:        
        for coord in self.posible_moves:
            self.set_button_bg(coord, 'SpringGreen2')
    
    
    def reset_highlight(self) -> None:
        for coord in self.posible_moves:
            self.reset_button_bg(coord)
            
        self.posible_moves = []
        
        
    def reset_params(self) -> None:
        self.dev_mode = False
        self.successfully = False
        self.turn = True
        self.delete_pending = False
        self.selected_coord = None
        self.selected_piece = None
        self.move_log.configure(state='normal')
        self.move_log.delete(1.0, tk.END)
        self.move_log.configure(state='disabled')
        
        
    def restart(self) -> None:
        if msgbox.askyesno('Restart', 'Are you sure you want to restart the game?'):
            self.board.reset_game()
            self.reset_params()
            for i in range(11):
                for j in range(11):
                    self.reset_button_bg(Coord(i, j))
            self.update_button()
            self.labels['message']['text'] = 'Game restarted'
            
            
    def test_ok(self) -> None:
        self.labels['message']['text'] = 'Test OK'