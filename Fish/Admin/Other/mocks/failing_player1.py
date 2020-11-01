import sys
sys.path.append('../Common/')
sys.path.append('../')
sys.path.append('../Admin/Other/')

from player import Player
from state import State
from position import Position


class FailingPlayer1(Player):
    """
    Implements a Player that makes no placements.
    """
    def get_placement(self, state: State) -> Position:
        # An integer is not a Position
        return 0xc0ff33
