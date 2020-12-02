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
    INTERPRETATION: The Server component is the the backend server that allows for remote players to connect
    to our machines in order to participate in tournaments and games of Fish.  Once run, the server will
    allow players to connect to our TCP server socket for a certain period of time.  Players who sign-up earlier will
    take their turns first in games.  We then instantiate a RemotePlayerProxy component for each player, for which 
    we will use to connect our TournamentManager / Referee to the remote players.  This is described in more detail
    in the RPP documentation.  We then run a full tournament with the set of players who have signed up, and output
    the results.

    PURPOSE: The Server component allows for remote clients to establish a TCP connection to our Fish admin servers,
    and participate in a tournament (and within it many games) of Fish.  It facilitates the creation of the tournament
    manager, creation of TCP client sockets to be passed to remote player proxies playing in the tournament, and thus

    DEFINITION(S):
    signup timeout      -> the number of seconds to wait for client sign ups within one signup period
    signup period       -> the action of waiting "signup timeout" seconds for players to establish a connection
                           and give name
    client              -> the remote player software that we are communicated with over the network
    server socket       -> this servers TCP socket at which we are accepting client connections
    remote player proxy -> our player implementation that supports communicating with remote players
    """
    DEBUG = False

    # How long to wait for client to respond to messages
    CLIENT_TIMEOUT = 1

    def __init__(self, signup_timeout: int = 30, min_clients: int = 5, max_clients: int = 10, signup_periods: int = 2):
        """
        Initializes a server component using various default parameters.

        :param signup_timeout: the number of seconds to wait for client signups in each waiting period
        :param min_clients: the minimum number of clients needed to stop signups and hand off to tournament manager
        :param max_clients: the max number of client signups needed to immediately exit the waiting phase and hand them off to the tournament manager
        :param signup_periods: the number of times to restart our signup_timeout length timer and wait for players (before shutting down if there are not enough players)
        """
        self._signup_timeout = signup_timeout
        self._min_clients = min_clients
        self._max_clients = max_clients
        self._signup_periods = signup_periods

        self._server_socket = None
        self._remote_player_proxies = []

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
        self._init_socket(port)
        # if the socket is created successfully, continue
        if self._server_socket:
            # listen for sign-ups
            self._signup_players()
            # runs a tournament
            w_cf = self._run_tournament()
            # tears down the tournament
            self._teardown_tournament()
            # [# winners, # cheaters + # failed]
            print(w_cf)

    def _init_socket(self, port: int):
        """
        Helper function to initialize a TCP server socket on the given port.  This socket will be used to accept client
        connections (player signups) until we have either determined that not enough players have signed up to play, or 
        enough players have signed up for a tournament to be run.

        :param port: the port to open the TCP server socket on (to accept client sign ups)
        :return a TCP server socket that is ready to accept client connections or None if unsuccessful
        """
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.settimeout(self._signup_timeout)

        try:
            server_sock.bind(('localhost', port))
            server_sock.listen(self._max_clients)
            self._server_socket = server_sock
        except Exception as e:
            print(e)

    def _signup_players(self):
        """
        Accept client connections (sign up players) for the specified number of sign up periods (and time per sign up period).
        A signup round will be conducted if we have not exhausted all waiting periods, or if we have hit the max_clients limit.
        """
        while self._signup_periods > 0 and len(self._remote_player_proxies) < self._min_clients and len(self._remote_player_proxies) != self._max_clients:
            self._run_signup_period()

        if Server.DEBUG:
            for rpp in self._remote_player_proxies:
                print(f'[SERV] Player {rpp.name} has been signed up (age = {rpp.age})')

    def _run_tournament(self):
        """
        Runs an entire tournament with the remote player proxies created during the signup phase. If the tournament is
        unable to be ran, a message will be printed explaining why. If the tournament completes successfully, then the
        number of winners and number of players kicked from the tournament is printed to the console.

        :return: None
        """
        if self._can_tournament_run():
            # create tournament manager with the player proxies
            tm_manager = Manager(self._remote_player_proxies)
            # For the purposes of logging tournament information as the tournament progresses
            if Server.DEBUG:
                tm_manager.subscribe_tournament_updates(self._log_tournament_update)
            tm_manager.run()
            return [len(tm_manager.tournament_winners), len(tm_manager.tournament_kicked)]
        else:
            print(f'Not enough or too many players signed up to run tournament...'
                  f' ({len(self._remote_player_proxies)} / {self._min_clients})')

    def _can_tournament_run(self) -> bool:
        """ 
        Check that the # of currently signed up players is between min and max (inclusive) 

        :return: whether a tournament can be run with the currently signed up players (True if yes)
        """
        return self._min_clients <= len(self._remote_player_proxies) <= self._max_clients

    def _run_signup_period(self):
        """
        This function conducts a single "waiting period" where we sign up players for a tournament throughn the server
        socket. It looks for new connections on our TCP server socket, and will add any client socket connections
        to our self._remote_player_proxies array. This function will wait for signups for self._signup_timeout 
        seconds before returning.
        """
        # get time in self._signup_timeout seconds from now
        time_end = time.time() + self._signup_timeout

        # loop until we reach that time (i.e. this loop will run for signup_timeout seconds)
        while time.time() < time_end:
            client_sock = None
            try:
                (client_sock, address) = self._server_socket.accept()
                client_sock.settimeout(self.CLIENT_TIMEOUT)

                # Receive name from client
                data = client_sock.recv(4096)

                name = data.decode('ascii')

                if name and self._is_name_available(name):
                    # client timeout is now handled by the referee
                    client_sock.settimeout(None)
                    # Initialize the remote proxy player with the client socket
                    curr_time = time.time()
                    rpp = RemotePlayerProxy(name, curr_time, client_sock)
                    self._remote_player_proxies.append(rpp)
                else:
                    # Either did not provide name, or provided a taken name, so we disconnect them
                    client_sock.close()

                # If we have reached the max number of clients, stop listening
                if len(self._remote_player_proxies) == self._max_clients:
                    break
            except Exception:
                if client_sock:
                    client_sock.close()

        self._signup_periods -= 1

    def _is_name_available(self, name: str) -> bool:
        """
        A helper to check if our server has already signed up a client with the given name.  This
        will be used to ensure that all players who sign up have unique names.

        :param name: the name to check for availability
        :return: true if the name is available for use (unused), else false
        """
        for rpp in self._remote_player_proxies:
            if rpp.name == name:
                return False
        return True

    def _teardown_tournament(self):
        """ Fired once the tournament is over, closes all open TCP socket connections """
        for rpp in self._remote_player_proxies:
            rpp.socket.close()
        self._server_socket.close()

    def _log_tournament_update(self, payload):
        """ For debugging, log NEW_ROUND and TOURNAMENT_END updates to stdout """
        if payload['type'] == TournamentUpdateType.NEW_ROUND:
            print(f'\n~~~~~ [NEW ROUND] [ROUND {payload["round_num"]}] Games = {payload["games"]} ~~~~~\n')
        elif payload['type'] == TournamentUpdateType.TOURNAMENT_END:
            print(f'\n~~~~~ [TOURNAMENT END] Winners = {payload["winners"]} ~~~~~\n')
        return True
