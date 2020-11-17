import sys

sys.path.append('../Common/')
sys.path.append('../')
sys.path.append('../Admin/Other/')

from player import Player
from action import Action
from player_status import PlayerStatus


class FailingWinner2(Player):
    """
    Implements a Player that loops forever in acknowledging that they won the tournament.
    """

    def status_update(self, state: PlayerStatus) -> Action:
        if state == PlayerStatus.WON_TOURNAMENT:
            while(True):
                pass
