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
        pass
    
    def promote(self):
        pass