class OutOfTilesException(Exception):
    """
    An exception signaling that the state is out of open
    tiles.
    """
    def __init__(self, msg=""):
        """
        Initializes exception.
        :param msg: exception message
        :return: new Exception object
        """
        super().__init__(msg)
