class AbstractTile(object):
    def __init__(self):
        self.__type = 'abstract'

    @property
    def type(self):
        return self.__type

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
