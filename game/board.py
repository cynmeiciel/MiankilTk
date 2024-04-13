from collections import defaultdict

from .coord import *
from .piece import *
from .tier0 import *
from .tier1 import *
from .tier2 import *
from .tier3 import *
from .tier4 import *

class Board:
    def __init__(self):
        self.reset_game()
       
        
    def reset_game(self) -> None:
        self.board = [[None for _ in range(11)] for _ in range(11)]
        
        self.dead_pieces = PieceCounter()
        self.on_hand_pieces = PieceCounter()
        
        self.init_board()
        
        
    def init_board(self) -> None:
        self.board[0][0] = Pawn(True)
        self.board[0][1] = Sentinel(True)
        self.board[4][2] = Scout(True)
        self.board[0][3] = Watcher(True)
        self.board[0][4] = Guard(True)
        self.board[5][0] = Nexus(True)
        
        self.board[10][10] = Pawn(False)
        self.board[10][9] = Sentinel(False)
        self.board[6][8] = Scout(False)
        self.board[10][7] = Watcher(False)
        self.board[10][6] = Guard(False)
        self.board[5][10] = Nexus(False)
    
    
    def find_piece(self, coord : Coord) -> Piece:
        return self.board[coord.x][coord.y]
    
    
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
        
        
    def get_all_pieces(self, is_blue) -> list[list]:
        pieces = []
        for i in range(11):
            for j in range(11):
                if self.board[i][j] is not None and self.board[i][j].is_blue == is_blue:
                    pieces.append([Coord(i, j), self.board[i][j]])
        return pieces
    
    
    def nexus_checked(self, is_blue) -> bool:
        all_pieces = self.get_all_pieces(not is_blue)
        for piece in all_pieces:
            if piece[1].can_move(self, piece[0], BLUE_NEXUS if is_blue else RED_NEXUS):
                return True
        return False
    
    
    def copy(self) -> 'Board':
        new_board = Board()
        for i in range(11):
            for j in range(11):
                new_board.board[i][j] = self.board[i][j]
        return new_board
    
    
    def move_piece(self, start : Coord, end : Coord) -> None:
            if dead:=self.board[end.x][end.y]:
                self.dead_pieces.append(dead, dead.is_blue)
            self.board[end.x][end.y] = self.board[start.x][start.y]
            self.board[start.x][start.y] = None



class PieceCounter:
    def __init__(self):
        self.pieces : dict[dict] = {
            'blue' : defaultdict(int),
            'red' : defaultdict(int)
        }
                
    def append(self, piece : Piece, is_blue : bool) -> None:
        self.pieces['blue' if is_blue else 'red'][piece] += 1

    def get(self, piece : type, is_blue : bool) -> Piece:
        side = 'blue' if is_blue else 'red'
        self.pieces[side][piece] -= 1
        
        return piece(is_blue)

    def __repr__(self):
        return f'Blue: {self.blue}\nRed: {self.red}'