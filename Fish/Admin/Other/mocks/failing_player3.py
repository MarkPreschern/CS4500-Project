import sys

sys.path.append('../Common/')
sys.path.append('../')
sys.path.append('../Admin/Other/')

from player import Player
from state import State
from action import Action


class FailingPlayer3(Player):
    """
    Implements a Player enters an infinite loop in making an action.
    """

    def get_action(self, state: State) -> Action:
        # A Position is not an Action
        while True:
            pass
        return b'c0ff33'
