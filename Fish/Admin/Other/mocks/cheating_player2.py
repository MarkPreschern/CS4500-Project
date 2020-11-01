import sys


sys.path.append('../Common/')
sys.path.append('../')
sys.path.append('../Admin/Other/')

from player import Player
from state import State
from position import Position
from action import Action


class CheatingPlayer2(Player):
    """
    Implements a Player that makes illegal actions.
    """
    def get_action(self, state: State) -> Action:
        # Return caffenaited action
        return Action(Position(0xc0ff33, 1337), Position(0xc0ff33, 1337))
