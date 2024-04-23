from typing import TYPE_CHECKING

from .coord import *
from .const import *
from .piece import *

if TYPE_CHECKING:
    from .board import Board

# TIER 0:
# NEXUS, CUSTODIAN

class Nexus(Piece):
    def __init__(self, is_blue):
        super().__init__(is_blue, 'Nexus')
    
    def can_move(self, board : 'Board', start : Coord, end : Coord):
        return False

class Custodian(Piece):
    def __init__(self, is_blue):
        super().__init__(is_blue, 'Custodian')
    
    def can_move(self, board : 'Board', start : Coord, end : Coord):
        return False

class Sentinel(Piece):
    def __init__(self, is_blue):
        super().__init__(is_blue, 'Sentinel')
    
    def can_move(self, board : 'Board', start : Coord, end : Coord):
        # Check if the start and end coordinates are not on the same column or row
        if start.x != end.x and start.y != end.y:
            return False
        if board.find_piece(end) is not None:
            return False
        
        return super().can_move(board, start, end) if start.dist_radius(end) <= 2 else False