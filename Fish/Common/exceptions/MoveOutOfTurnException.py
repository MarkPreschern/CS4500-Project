class MoveOutOfTurnException(Exception):
    """
    An exception signaling that a player has
    attempted to make a move out of turn.
    """

    def __init__(self, msg=""):
        """
        Initializes exception.
        :param msg: exception message
        :return: new Exception object
        """
        super().__init__(msg)
