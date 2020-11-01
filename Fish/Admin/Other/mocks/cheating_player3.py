import sys


sys.path.append('../Common/')
sys.path.append('../')
sys.path.append('../Admin/Other/')

from player import Player
from state import State
from action import Action


class CheatingPlayer3(Player):
    """
    Implements a Player that makes the illegal action of moving in-place.
    """
    def get_action(self, state: State) -> Action:
        # Determine where we are
        pos = state.placements[state.current_player][0]
        # Move in-place
        return Action(pos, pos)
