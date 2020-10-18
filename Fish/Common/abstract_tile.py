class AbstractTile(object):
    """
    Represents the base to either a hole or a tile.
    """
    @property
    def is_hole(self):
        """
        Checks whether object is a hole.
        """
        return False

    @property
    def is_tile(self):
        """
        Checks whether object is a tile.
        """
        return False

    @property
    def fish_no(self):
        """
        Retrieves the number of fish to the tile.
        """
        return 0
