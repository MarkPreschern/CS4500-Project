import sys

sys.path.append('../Common/')
sys.path.append('../')
sys.path.append('../Admin/Other/')

from player import Player
from state import State
from action import Action


class FailingPlayer5(Player):
    """
    Implements a Player runs an infinite loop in making a placement.
    """

    def get_placement(self, state: State) -> Action:
        # A Position is not an Action
        while True:
            pass
        return b'c0ff33'
