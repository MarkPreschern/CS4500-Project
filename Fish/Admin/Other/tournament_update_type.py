from enum import Enum


class TournamentUpdateType(Enum):
    """
    Enum that denotes the type of tournament update
    dispatched to tournament observers.
    """
    NEW_ROUND = 0,
    TOURNAMENT_END = 1
