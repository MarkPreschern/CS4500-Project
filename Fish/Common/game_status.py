from enum import Enum


class GameStatus(Enum):
    """
    GameStatus tells the state the game is in.
    """
    PLACING = 0,
    RUNNING = 1,
    OVER = 2
