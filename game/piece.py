from . import coord
from . import const

class Piece:
    def __init__(self, color, name):
        self.color = color
        self.name = name
        
    def __repr__(self):
        return self.name
        
    def can_move(self, board, start, end):
        return False
    
    def promote(self):
        pass