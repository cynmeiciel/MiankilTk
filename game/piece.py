from .coord import *
from .const import *

class Piece:
    def __init__(self, is_blue, name):
        self.is_blue = is_blue
        self.name = name
        
    def __repr__(self):
        return self.name
        
    def can_move(self, board, start, end):
        return False
    
    def promote(self):
        pass