from enum import Enum
from .coord import Coord

BWIDTH = 11
BHEIGHT = 11

BLUE_NEXUS = Coord(5, 0)
RED_NEXUS = Coord(5, 10)

DE = 'slategray1' # default
SP = 'deepskyblue4' # split
RI = 'skyblue' # river
FO = 'forest green' # forest

SQUARE_COLORS : list[list[str]] = [
    [DE, DE, DE, SP, DE, DE, DE, RI, DE, DE, DE],
    [DE, DE, DE, SP, DE, DE, DE, RI, DE, DE, DE],
    [DE, DE, DE, SP, DE, DE, DE, RI, DE, DE, DE],
    [SP, SP, SP, SP, SP, SP, SP, RI, SP, SP, SP],
    [DE, DE, DE, SP, DE, DE, DE, RI, DE, DE, DE],
    [DE, DE, DE, RI, RI, RI, RI, RI, DE, DE, DE],
    [DE, DE, DE, RI, DE, DE, DE, SP, DE, DE, DE],
    [SP, SP, SP, RI, SP, SP, SP, SP, SP, SP, SP],
    [DE, DE, DE, RI, DE, DE, DE, SP, DE, DE, DE],
    [DE, DE, DE, RI, DE, DE, DE, SP, DE, DE, DE],
    [DE, DE, DE, RI, DE, DE, DE, SP, DE, DE, DE]
]
    
        
class CellType(Enum):
    pass

class Ability(Enum):
    pass

class PieceType(Enum):
    pass
    
