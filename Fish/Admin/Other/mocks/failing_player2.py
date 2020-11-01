import sys


sys.path.append('../Common/')
sys.path.append('../')
sys.path.append('../Admin/Other/')

from player import Player
from state import State
from position import Position
from action import Action


class FailingPlayer2(Player):
    """
    Implements a Player that makes no actions.
    """
    def get_action(self, state: State) -> Action:
        # A Position is not an Action
        return Position(0, 1)
