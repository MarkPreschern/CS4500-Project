class GameNotStartedException(Exception):
    """
    An exception signaling that the game has not
    started.
    """
    def __init__(self, msg=""):
        """
        Initializes exception.
        :param msg: exception message
        :return: new Exception object
        """
        super().__init__(msg)
