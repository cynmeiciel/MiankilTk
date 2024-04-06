class Piece:
    def __init__(self, color, name):
        self.color = color
        self.name = name
        
    def __repr__(self):
        return self.name
        
    def can_move(self, board, start, end):
        return True
    
    def promote(self):
        pass

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, '♟')
    
    def can_move(self, start, end):
        # Check if the start and end coordinates are not on the same column
        if start.x != end.x:
            return False
        
        # Check if the move is one cell forward
        if abs(start.y - end.y) != 1:
            return False
        
        # Check if the move is forward
        if self.color == 'white' and start.y >= end.y:
            return False
        
        if self.color == 'black' and start.y <= end.y:
            return False
        
        return True