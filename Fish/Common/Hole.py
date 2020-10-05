from AbstractTile import AbstractTile


class Hole(AbstractTile):
    """
    Represents a gap in the game board.
    """
    def __init__(self):
        super().__init__()

        # Set type
        self.__type = 'hole'

    @property
    def is_hole(self):
        return True

    @property
    def is_tile(self):
        return False
