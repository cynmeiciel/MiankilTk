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
        
    def can_move(self, board : 'Board', start : Coord, end : Coord):
        piece = board.find_piece(end)
        ENEMY_NEXUS = RED_NEXUS if self.is_blue else BLUE_NEXUS
        if end == ENEMY_NEXUS:
            return True
        
        if piece is not None and piece.is_blue == self.is_blue:
            return False
        
        new_board = board.copy()
        new_board.move_piece(start, end)
        return not new_board.nexus_checked(self.is_blue)
    
    def get_moves(self, board : 'Board', start : Coord) -> list[Coord]:
        moves = []
        for i in range(11):
            for j in range(11):
                if self.can_move(board, start, Coord(i, j)):
                    moves.append(Coord(i, j))
        return moves
    
    def promote(self):
        pass
