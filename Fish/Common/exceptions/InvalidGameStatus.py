class InvalidGameStatus(Exception):
    """
    An exception signaling that the game status is different than what
    was expected.
    """
    def __init__(self, msg=""):
        """
        Initializes exception.
        :param msg: exception message
        :return: new Exception object
        """
        super().__init__(msg)
