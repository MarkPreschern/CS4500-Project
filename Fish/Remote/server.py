import socket
import time

from remote_player_proxy import RemotePlayerProxy

class Server(object):
    """
    INTERPRETATION: TODO.

    PURPOSE: TODO.

    DEFINITION(S): TODO.
    """

    def __init__(self, signup_timeout: int = 30, min_clients: int = 5, max_clients: int = 10, waiting_periods: int = 1):
        """
        Initializes a server component using various default parameters.

        :param signup_timeout: the number of seconds to wait for client signups in each waiting period
        :param min_clients: the minimum number of clients needed to stop signups and hand off to tournament manager
        :param max_clients: the max number of client signups needed to immediately exit the waiting phase and hand them off to the tournament manager
        :param waiting_periods: the number of times to restart our signup_timeout length timer and wait for players (before shutting down if there are not enough players)
        """
        self.__signup_timeout = signup_timeout
        self.__min_clients = min_clients
        self.__max_clients = max_clients
        self.__waiting_periods = waiting_periods

        self.__is_signup_phase = True
        self.__remote_player_proxies = []

    def run(self, port: int):
        """
        The "main" method of the server.
        It starts a server socket and listens for clients. If enough players sign up for a tournamant, it hands the
        signed-up players off to the tournament manager for this purpose, runs the tournament, communicates with the players,
        and gracefully shuts down after the tournament is over.  If not enough players sign up, it will gracefully shut down 
        without playing a tournament.

        :param port: the port to open the server socket on (to accept client sign ups)
        """
        # create server socket on given port
        self.__server_socket = self.__init_socket(port)

        # (in a loop) listen for signups
        self.__signup_players()

        for rpp in self.__remote_player_proxies:
            print(f'Player {rpp.name} has been signed up (age = {rpp.age})')

    def __init_socket(self, port: int) -> socket:
        """
        Helper function to initialize a TCP server socket on the given port.  This socket will be used to accept client
        connections (player signups) until we have either determined that not enough players have signed up to play, or 
        enough players have signed up for a tournament to be run.

        :param port: the port to open the TCP server socket on (to accept client sign ups)
        :return a TCP server socket that is ready to accept client connections or None if unsuccessful
        """
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.settimeout(self.__signup_timeout)

        try:
            server_sock.bind(('localhost', port))
            server_sock.listen(self.__max_clients)
            return server_sock
        except Exception:
            return None

    def __signup_players(self):
        """
        Accept client connections (sign up players) for the specified number of sing up periods (and time per sign up period)

        :return all of the TCP client connections that have been established during the sign up phase of this server.
        """
        while self.__waiting_periods > 0 or len(self.__remote_player_proxies) < self.__min_clients:
            self.__run_signup_period()

        self.__is_signup_phase = False

    def __run_signup_period(self):
        """
        This function conducts a single "waiting period" where we sign up players for a tournament throught the server
        socket. It looks for new connections on our TCP server socket, and will add any client socket connections
        to our self.__remote_player_proxies array. This function will wait for signups for self.__signup_timeout seconds before returning.

        :return the TCP client sockets that were "signed up" in this sign up period
        """
        # get time in self.__signup_timeout seconds from now
        time_end = time.time() + self.__signup_timeout

        # loop until we reach that time (i.e. this loop will run for signup_timeout seconds)
        while time.time() < time_end:
            try:
                (client_sock, address) = self.__server_socket.accept()
                data = client_sock.recv(4096)

                if data:
                    curr_time = time.time()
                    rpp = RemotePlayerProxy(data.decode('utf-8'), curr_time, client_sock)
                    self.__remote_player_proxies.append(rpp)

                # If we have reached the max number of clients, stop listening
                if len(self.__remote_player_proxies) == self.__max_clients:
                    break
            except socket.timeout:
                break

        self.__waiting_periods -= 1
