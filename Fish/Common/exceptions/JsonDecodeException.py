class JsonDecodeException(Exception):
    """
    An exception signaling that we attempted to decode an invalid JSON message.
    """
    def __init__(self, msg=""):
        """
        Initializes exception.
        :param msg: exception message
        :return: new Exception object
        """
        super().__init__(msg)
