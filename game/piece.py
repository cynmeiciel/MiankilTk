from typing import TYPE_CHECKING

from .coord import *
from .const import *

if TYPE_CHECKING:
    from .board import Board

class Piece:
    def __init__(self, is_blue, name):
        self.is_blue = is_blue
        self.name = name
        
    def __repr__(self):
        return self.name
        
    def can_move(self, board : 'Board', end : Coord):
        piece = board.find_piece(end)
        if piece is not None and piece.is_blue == self.is_blue:
            return False
        
        return True
    
    def get_moves(self, board : 'Board', start : Coord) -> list[Coord]:
        moves = []
        for i in range(11):
            for j in range(11):
                if self.can_move(board, start, Coord(i, j)):
                    moves.append(Coord(i, j))
        return moves
    
    def promote(self):
        pass
