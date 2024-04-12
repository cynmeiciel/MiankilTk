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
        super().__init__(is_blue, 'NEX')
    
    def can_move(self, board : 'Board', start : Coord, end : Coord):
        return False

class Custodian(Piece):
    def __init__(self, is_blue):
        super().__init__(is_blue, 'CUS')
    
    def can_move(self, board : 'Board', start : Coord, end : Coord):
        return False