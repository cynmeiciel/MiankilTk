from typing import TYPE_CHECKING

from .coord import *
from .const import *
from .piece import *

if TYPE_CHECKING:
    from .board import Board

# TIER 2:
# VANGUARD, COMMANDER, TRAILBLAZER, STRATEGIST, BULWARK, TEMPLAR

class Vanguard(Piece):
    pass

class Commander(Piece):
    pass

class Trailblazer(Piece):
    pass

class Strategist(Piece):
    pass

class Bulwark(Piece):
    pass

class Templar(Piece):
    pass