from enum import Enum


class PlayerStatus(Enum):
    """
    This enum describes the status of a Player at the end of a game of Fish.
    """
    WON_GAME = 0,
    LOST_GAME = 1,
    WON_TOURNAMENT = 2,
    DISCONTINUED = 3
