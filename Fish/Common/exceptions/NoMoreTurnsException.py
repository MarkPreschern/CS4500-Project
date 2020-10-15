class NoMoreTurnsException(Exception):
    """
    An exception signaling that there are no more turns
    is invalid.
    """
    def __init__(self, msg=""):
        """
        Initializes exception.
        :param msg: exception message
        :return: new Exception object
        """
        super().__init__(msg)
