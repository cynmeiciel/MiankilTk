from enum import Enum

BWIDTH = 11
BHEIGHT = 11

class CellType(Enum):
    pass

class Ability(Enum):
    pass

class PieceType(Enum):
    pass

class Turn(Enum):
    BLUE = 1
    BLUE_SELECTED = 2
    RED = 3
    RED_SELECTED = 4
    
    