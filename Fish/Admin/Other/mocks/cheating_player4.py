import sys


sys.path.append('../Common/')
sys.path.append('../')
sys.path.append('../Admin/Other/')

from player import Player
from state import State
from action import Action


class CheatingPlayer4(Player):
    """
    Implements a Player that makes the illegal action of moving to another
    avatar (already occupied tile) on a possibly not straight or clear path.
    """
    def get_action(self, state: State) -> Action:
        # Determine where we are
        from_pos = state.placements[state.current_player][0]
        to_pos = state.placements[state.current_player][1]

        # Move in-place
        return Action(from_pos, to_pos)
