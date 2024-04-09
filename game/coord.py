class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)
    
    def __eq__(self, other):
        try:
            return self.x == other.x and self.y == other.y
        except AttributeError:
            return False
    
    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'
    
    def abs(self):
        return Coord(abs(self.x), abs(self.y))
    
    def dist_radius(self, other):
        return max(abs(self.x - other.x), abs(self.y - other.y))
    
    def dist_direc_y(self, is_blue : bool, end : 'Coord') -> int:
        if is_blue:
            return end.y - self.y
        else:
            return self.y - end.y