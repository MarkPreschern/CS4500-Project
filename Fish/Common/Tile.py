from AbstractTile import AbstractTile


class Tile(AbstractTile):
    """
    Represents a tile in the game onto which fish rest.
    """
    def __init__(self, fish_no):
        # Validate params
        if not isinstance(fish_no, int) or fish_no < 1:
            raise ValueError('Invalid fish_no - expected a positive integer!')

        # Set # of fish
        self.__fish_no = fish_no

    @property
    def fish_no(self):
        """
        Retrieves the number of fish to the tile.
        """
        return self.__fish_no
