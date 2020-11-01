import sys
sys.path.append('../Common/')
sys.path.append('../')
sys.path.append('../Admin/Other/')

from player import Player
from state import State
from position import Position


class CheatingPlayer1(Player):
    """
    Implements a Player that makes illegal placements.
    """
    def get_placement(self, state: State) -> Position:
        # I love coffee, but it ain't no valid Position
        return Position(0xc0ff33, 1337)
