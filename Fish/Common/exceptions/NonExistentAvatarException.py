class NonExistentAvatarException(Exception):
    """
    An exception signaling that the avatar
    is non existent.
    """
    def __init__(self, msg=""):
        """
        Initializes exception.
        :param msg: exception message
        :return: new Exception object
        """
        super().__init__(msg)
