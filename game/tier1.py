from .coord import *
from .piece import *

# TIER 1:
# PAWN, SENTINEL, SCOUT, WATCHER, GUARD

class Pawn(Piece):
    def __init__(self, is_blue):
        super().__init__(is_blue, '♟')
    
    def can_move(self, start : Coord, end : Coord):
        # Check if the start and end coordinates are not on the same column
        if start.x != end.x:
            return False
        
        # Check if the move is one cell forward
        if abs(start.y - end.y) != 1:
            return False
        
        # Check if the move is forward
        if self.is_blue and start.y >= end.y:
            return False
        
        if not self.is_blue and start.y <= end.y:
            return False
        
        return True