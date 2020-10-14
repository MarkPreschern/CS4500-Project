class NonExistentPlayerException(Exception):
    """
    An exception signaling that the player
    is non existent.
    """
    def __init__(self, msg=""):
        """
        Initializes exception.
        :param msg: exception message
        :return: new Exception object
        """
        super().__init__(msg)
