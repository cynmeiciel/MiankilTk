from .coord import *
from .piece import *
from .tier0 import *
from .tier1 import *
from .tier2 import *
from .tier3 import *
from .tier4 import *

class Board:
    def __init__(self):
        self.board = [[None for _ in range(11)] for _ in range(11)]
        
        self.init_board()
        
    def init_board(self) -> None:
        self.board[0][0] = Pawn(True)
        self.board[0][1] = Sentinel(True)
        self.board[4][2] = Scout(True)
        self.board[0][3] = Watcher(True)
        self.board[0][4] = Guard(True)
    
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

