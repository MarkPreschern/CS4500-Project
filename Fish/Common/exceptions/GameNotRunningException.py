class GameNotRunningException(Exception):
    """
    An exception signaling that the game is not running.
    """
    def __init__(self, msg=""):
        """
        Initializes exception.
        :param msg: exception message
        :return: new Exception object
        """
        super().__init__(msg)
