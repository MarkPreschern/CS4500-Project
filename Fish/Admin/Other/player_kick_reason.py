from enum import Enum


class PlayerKickReason(Enum):
    """
    Represents the reason a Player was removed from the game.
    """
    CHEATING = 1
    FAILING = 2
