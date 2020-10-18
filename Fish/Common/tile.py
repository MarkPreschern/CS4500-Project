from abstract_tile import AbstractTile
import constants as ct


class Tile(AbstractTile):
    """
    Represents a tile in the game onto which fish or players rest.
    """

    def __init__(self, fish_no: int):
        super().__init__()
        # Validate params
        if not isinstance(fish_no, int) or fish_no < ct.MIN_FISH_PER_TILE \
                or fish_no > ct.MAX_FISH_PER_TILE:
            raise ValueError('Invalid fish_no - expected a positive integer!')

        # Set # of fish
        self.__fish_no = fish_no

    @property
    def fish_no(self):
        """
        Retrieves the number of fish to the tile.
        """
        return self.__fish_no

    @property
    def is_hole(self):
        return False

    @property
    def is_tile(self):
        return True
