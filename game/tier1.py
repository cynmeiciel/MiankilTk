from typing import TYPE_CHECKING

from .coord import *
from .const import *
from .piece import *

if TYPE_CHECKING:
    from .board import Board

# TIER 1:
# PAWN, SENTINEL, SCOUT, WATCHER, GUARD

class Pawn(Piece):
    def __init__(self, is_blue):
        super().__init__(is_blue, 'Pawn')
    
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

class Sentinel(Piece):
    def __init__(self, is_blue):
        super().__init__(is_blue, 'Sentinel')
    
    def can_move(self, start : Coord, end : Coord):
        # Check if the start and end coordinates are not on the same column or row
        if start.x != end.x and start.y != end.y:
            return False
        
        return True if start.dist_radius(end) == 2 else False
    
class Scout(Piece):
    def __init__(self, is_blue):
        super().__init__(is_blue, 'Scout')
    
    # Moves in an "L" shape, but cannot move backwards
    def can_move(self, start: Coord, end: Coord):
        distx = abs(start.x - end.x)
        disty = start.dist_direc_y(self.is_blue, end)
        
        if distx == 2 and disty == 1:
            return True
        elif distx == 1 and disty == 2:
            return True
        
        return False
        
        
    
class Watcher(Piece):
    def __init__(self, is_blue):
        super().__init__(is_blue, 'Watcher')
    
    def can_move(self, start : Coord, end : Coord):
        if (diag:=abs(start.x - end.x)) == abs(start.y - end.y):
            return True if diag <= 2 else False
    
class Guard(Piece):
    def __init__(self, is_blue):
        super().__init__(is_blue, 'Guard')
    
    def can_move(self, start : Coord, end : Coord):
        return True if start.dist_radius(end) == 1 else False