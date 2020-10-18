class InvalidActionException(Exception):
    """
    An exception signaling that the action
    is invalid.
    """
    def __init__(self, msg=""):
        """
        Initializes exception.
        :param msg: exception message
        :return: new Exception object
        """
        super().__init__(msg)
