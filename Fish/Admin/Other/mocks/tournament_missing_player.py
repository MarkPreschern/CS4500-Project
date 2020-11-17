import sys

sys.path.append('../Common/')
sys.path.append('../')
sys.path.append('../Admin/Other/')

from player import Player
from action import Action


class TournamentMissingPlayer(Player):
    """
    Implements a Player that fails to acknowledge the start of a tournament.
    """

    def tournament_has_started(self) -> Action:
        return False
