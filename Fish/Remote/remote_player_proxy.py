import socket

class RemotePlayerProxy(object):
    """
    INTERPRETATION: TODO.

    PURPOSE: TODO.

    DEFINITION(S): TODO.
    """

    def __init__(self, name: str, age: float, socket: socket):
        """
        Initializes a remote player proxy with a name, age, and TCP client socket.

        :param name: name is a string that will act as a unique identifier of this player on the Fish servers
        :param age: the time in seconds since the epoch at the point when our server signed this player up (the lower this number, the "younger" the player)
        :param socket: the client TCP socket that will allow our server to communicate with this player
        """
        self.__name = name
        self.__age = age
        self.__socket = socket

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    @property
    def socket(self):
        return self.__socket