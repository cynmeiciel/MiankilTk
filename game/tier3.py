from typing import TYPE_CHECKING

from .coord import *
from .const import *
from .piece import *

if TYPE_CHECKING:
    from .board import Board

# TIER 3:
# KNIGHT, ASSASSIN, MAGE, ARCHER, SPIRITUALIST

class Knight(Piece):
    pass

class Assassin(Piece):
    pass

class Mage(Piece):
    pass

class Archer(Piece):
    pass

class Spiritualist(Piece):
    pass