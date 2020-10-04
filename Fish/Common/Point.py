class Point:
    """
    Represents a point in a 2D coordinate system.
    """
    def __init__(self, x, y):
        """
        Initializes a Point object.
        """
        # Check params
        if not isinstance(x, int):
            raise ValueError('Expected a positive integer for x!')

        if not isinstance(y, int):
            raise ValueError('Expected a positive integer for y!')

        # Set properties
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

djdjhell

dkd