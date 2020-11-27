import socket

class Client(object):
    """
    INTERPRETATION: TODO.

    PURPOSE: TODO.

    DEFINITION(S): TODO.
    """

    def __init__(self, name: str):
        """
        Initializes a client with the given name, for the purpose of connecting to the Fish servers and playing
        in a tournament of fish.

        :param name: name is a string that will act as a unique identifier of this player on the Fish servers
        """
        self.__name = name

    def run(self, host: str, port: int):
        """
        Connect to Fish servers and participate in a tournament of Fish.  This involves establishing an initial
        TCP connection with Fish servers, providing our player name, and then handling messages from server
        accordingly to allow us to play through sequential games of Fish in the tournament (and receive messaging
        about how we are performing).
        """
        self.__client_sock = self.__init_socket(host, port)
        if self.__client_sock:
            self.__client_sock.send(bytes(self.__name, 'utf-8'))

        # TODO: await messages from server and play in tournament
        

    def __init_socket(self, host: str, port: int):
        """
        Creates a client TCP socket connected to the given host and port. If this fails, it returns None.
        """
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_sock.connect((host, port))
            return client_sock
        except Exception:
            return None