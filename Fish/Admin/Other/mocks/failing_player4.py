import sys

sys.path.append('../Common/')
sys.path.append('../')
sys.path.append('../Admin/Other/')

from player import Player
from state import State
from action import Action


class FailingPlayer4(Player):
    """
    Implements a Player that throws an Exception in making an action.
    """

    def get_action(self, state: State) -> Action:
        # A Position is not an Action
        raise TabError('Random exception!')
