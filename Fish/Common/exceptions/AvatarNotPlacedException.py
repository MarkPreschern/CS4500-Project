class AvatarNotPlacedException(Exception):
    """
    An exception signaling that an avatar has not been
    placed.
    """
    def __init__(self, msg=""):
        """
        Initializes exception.
        :param msg: exception message
        :return: new Exception object
        """
        super().__init__(msg)
