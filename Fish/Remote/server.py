import socket
import time
import sys

sys.path.append('../Fish/Admin')
sys.path.append('../Fish/Admin/Other')

from manager import Manager
from remote_player_proxy import RemotePlayerProxy
from tournament_update_type import TournamentUpdateType

class Server(object):
    """
    INTERPRETATION: TODO.

    PURPOSE: The Server component allows for remote clients to establish a TCP connection to our Fish admin servers,
    and participate in a tournament (and within it many games) of Fish.  It facilitates the creation of the tournament
    manager, creation of TCP client sockets to be passed to remote player proxies playing in the tournament, and thus

    DEFINITION(S):
    signup timeout -> the number of seconds to wait for client sign ups within one signup period
    signup period -> the action of waiting "signup timeout" seconds for players to establish a connection and give name
    client -> the remote player software that we are communicated with over the network
    server socket -> this servers TCP socket at which we are accepting client connections
    remote player proxy -> our player implementation that supports communicating with remote players
    """
    DEBUG = False

    def __init__(self, signup_timeout: int = 5, min_clients: int = 5, max_clients: int = 10, signup_periods: int = 1):
        """
        Initializes a server component using various default parameters.

        :param signup_timeout: the number of seconds to wait for client signups in each waiting period
        :param min_clients: the minimum number of clients needed to stop signups and hand off to tournament manager
        :param max_clients: the max number of client signups needed to immediately exit the waiting phase and hand them off to the tournament manager
        :param signup_periods: the number of times to restart our signup_timeout length timer and wait for players (before shutting down if there are not enough players)
        """
        self.__signup_timeout = signup_timeout
        self.__min_clients = min_clients
        self.__max_clients = max_clients
        self.__signup_periods = signup_periods
        self.__remote_player_proxies = []

    def run(self, port: int):
        """
        The "main" method of the server.
        It starts a server socket and listens for clients. If enough players sign up for a tournamant, it hands the
        signed-up players off to the tournament manager for this purpose, runs the tournament, and gracefully shuts 
        down after the tournament is over.  If not enough players sign up, it will gracefully shut down 
        without playing a tournament.

        :param port: the port to open the server socket on (to accept client sign ups)
        """
        # create server socket on given port
        self.__server_socket = self.__init_socket(port)

        # listen for signups
        self.__signup_players()

        if Server.DEBUG:
            for rpp in self.__remote_player_proxies:
                print(f'[SERV] Player {rpp.name} has been signed up (age = {rpp.age})')

        tm_manager = Manager(self.__remote_player_proxies)
        # For the purposes of logging tournament information as the tournament progresses

        if Server.DEBUG:
            tm_manager.subscribe_tournament_updates(self.__log_tournament_update)

        tm_manager.run()
        
        print([len(tm_manager.tournament_winners), len(tm_manager.tournament_kicked)])
        
        self.__teardown_tournament()

    def __teardown_tournament(self):
        """ Fired once the tournament is over, closes all open TCP socket connections """
        for rpp in self.__remote_player_proxies:
            rpp.socket.close()
        self.__server_socket.close()

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
        except Exception as e:
            print(e)
            return None

    def __signup_players(self):
        """
        Accept client connections (sign up players) for the specified number of sign up periods (and time per sign up period).
        A signup round will be conducted if we have not exhausted all waiting periods, or if we have hit the max_clients limit.
        """
        # Add case for if we hit max (?)
        while self.__signup_periods > 0 or len(self.__remote_player_proxies) < self.__min_clients:
            self.__run_signup_period()

    def __run_signup_period(self):
        """
        This function conducts a single "waiting period" where we sign up players for a tournament throughn the server
        socket. It looks for new connections on our TCP server socket, and will add any client socket connections
        to our self.__remote_player_proxies array. This function will wait for signups for self.__signup_timeout 
        seconds before returning.
        """
        # get time in self.__signup_timeout seconds from now
        time_end = time.time() + self.__signup_timeout

        # loop until we reach that time (i.e. this loop will run for signup_timeout seconds)
        while time.time() < time_end:
            try:
                (client_sock, address) = self.__server_socket.accept()

                # Receive name from client
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

        self.__signup_periods -= 1

    def __log_tournament_update(self, payload):
        """ For debugging, log NEW_ROUND and TOURNAMENT_END updates to stdout """
        if (payload['type'] == TournamentUpdateType.NEW_ROUND):
            print(f'\n~~~~~ [NEW ROUND] [ROUND {payload["round_num"]}] Games = {payload["games"]} ~~~~~\n')
        elif (payload['type'] == TournamentUpdateType.TOURNAMENT_END):
            print(f'\n~~~~~ [TOURNAMENT END] Winners = {payload["winners"]} ~~~~~\n')
        return True
    
