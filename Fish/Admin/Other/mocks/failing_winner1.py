import sys

sys.path.append('../Common/')
sys.path.append('../')
sys.path.append('../Admin/Other/')

from player import Player
from action import Action
from player_status import PlayerStatus


class FailingWinner1(Player):
    """
    Implements a Player that throws an Exception in acknowledging that they won tournament.
    """

    def status_update(self, state: PlayerStatus) -> Action:
        if state == PlayerStatus.WON_TOURNAMENT:
            # A Position is not an Action
            raise IndexError()
