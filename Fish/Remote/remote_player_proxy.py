import socket
import sys

sys.path.append('../Fish/Common')

from state import State
from position import Position
from action import Action
from color import Color
from player_status import PlayerStatus
from player_interface import IPlayer
from json_serializer import JsonSerializer

class RemotePlayerProxy(IPlayer):
    """
    TODO Add description of how we fail players in this component (and deal with abnormal conditions), once we do that

    INTERPRETATION: The remote player proxy is an implementation of our IPlayer interface that allows
    for a remote player to participate in games and tournaments of Fish.  When the referee our tournament manager
    makes a call to this players functions (i.e. requesting a placement), the remote player proxy will encode
    this request into a JSON protocol (see JsonSerializer documentation), and send it along to the remote client (player)
    it represents.  The client, also knowing this protocol, is able to decode the JSON message, calculate its placement,
    and send it back over the socket to this RPP.  This RPP then informs the referee (or tournament manager) of the remote
    player's request.

    PURPOSE: The purpose of the Remote Player Proxy is to allow for remote clients to connect to our servers and participate
    in games and tournaments of Fish, while our admin server can view them as simply any other player.  Therefore,
    this remote player proxy handles any abnormal conditions that may arise in the networked communications with the
    remote client.

    DEFINITION(S):
    RPP -> remote player proxy
    socket -> the TCP socket that allows this RPP to communicate with the remote player it represents
    age -> time in seconds (since epoch) noted when this player signed up with our server (we interpret
    this as the players age, and lower aged players are allocated to games first and take turns first)
    """
    DEBUG = False

    def __init__(self, name: str, age: float, socket: socket):
        """
        Initializes a remote player proxy with a name, age, and TCP client socket. Also
        initializes this players color to None (will be set when they enter their first game),
        and initializes a JSON serializer for the purpose of sending and receiving JSON messages
        from the remote player.

        :param name: name is a string that will act as a unique identifier of this player on the Fish servers
        :param age: see definitions above
        :param socket: the client TCP socket that will allow our server to communicate with this player
        """
        self.__name = name
        self.__age = age
        self.__socket = socket
        self.__color = None
        self.__json_serializer = JsonSerializer()

    def __receive_messages(self) -> str:
        """ 
        Receive JSON string message(s) from the remote player proxy and decode into a JSON-like Python object
        See JsonSerializer for details about this protocol, and communication process. 

        :return: a list of JSON string messages
        """
        while True:
            try:
                data = self.__socket.recv(4096)
                if data:
                    msgs = self.__json_serializer.bytes_to_jsons(data)
                    if RemotePlayerProxy.DEBUG:
                        for msg in msgs:
                            print(f'[RPP] [RECV] <- [{self.name}]: {msg}')
                    return msgs
            except Exception as e:
                print(e)
                return None

    def __send_message(self, data):
        """
        Send a JSON protocol message (string) through the socket connection. See JsonSerializer for details
        about this protocol, and communication process.
        
        :param sock: a socket object connected to a port
        :param data: the data to be sent
        """
        if RemotePlayerProxy.DEBUG:
            print(f'[RPP] [SEND] -> [{self.name}]: {data}')

        try:
            self.__socket.sendall(bytes(data, 'utf-8'))
        except Exception as e:
            print(e)

    def get_placement(self, state: State) -> Position:
        """ Implements PlayerInterface.get_placement(State). """
        # Validate params
        if not isinstance(state, State):
            raise TypeError('Expected State for state!')

        msg = self.__json_serializer.encode_setup(state)
        self.__send_message(msg)

        position_msgs = self.__receive_messages()
        if len(position_msgs) > 0:
            return self.__json_serializer.decode_position(position_msgs[0])
        else:
            return None

    def get_action(self, state: State) -> Action:
        """ Implements PlayerInterface.get_action(State). """
        # Validate params
        if not isinstance(state, State):
            raise TypeError('Expected State for state!')

        msg = self.__json_serializer.encode_take_turn(state)
        self.__send_message(msg)

        take_turn_msgs = self.__receive_messages()
        action = self.__json_serializer.decode_take_turn_response(take_turn_msgs[0])
        return action

    def kick(self, reason: str) -> None:
        """ Implements PlayerInterface.kick_player(str) """
        # Validate params
        if not isinstance(reason, str):
            raise TypeError('Expected str for state!')

        if RemotePlayerProxy.DEBUG:
            print(f'[{self.name}] was kicked for {reason}!')

        return None

    def sync(self, state: State) -> None:
        """ Implements PlayerInterface.sync(State) """
        # Validate params
        if not isinstance(state, State):
            raise TypeError('Expected State for state!')

        # Update internal state
        self.__state = state
        # A real player may decide what to do with this information, but an A.I. will use
        # the state received via get_action and get_placement to decide on a response.
        return None

    def game_over(self, leaderboard: list, cheating_players: list, failing_players: list) -> None:
        """ Implements PlayerInterface.game_over(dict, list, list). """
        # Validate params
        if not isinstance(leaderboard, list):
            raise TypeError('Expected list for leaderboard!')

        if not isinstance(cheating_players, list):
            raise TypeError('Expected list for cheating_players!')

        if not isinstance(failing_players, list):
            raise TypeError('Expected list for failing_players!')

        return None
        

    def status_update(self, status: PlayerStatus) -> bool:
        """ Implements PlayerInterface.status_update(PlayerStatus) """
        if not isinstance(status, PlayerStatus):
            raise TypeError('Expected PlayerStatus for status!')
        
        if status == PlayerStatus.LOST_GAME:
            msg = self.__json_serializer.encode_tournament_end(False)
            self.__send_message(msg)
        elif status == PlayerStatus.DISCONTINUED:
            msg = self.__json_serializer.encode_tournament_end(False)
            self.__send_message(msg)
        elif status == PlayerStatus.WON_TOURNAMENT:
            msg = self.__json_serializer.encode_tournament_end(True)
            self.__send_message(msg)
        return True

    def set_color(self, color: Color):
        """ Implements PlayerInterface.set_color() """
        self.__color = color
        msg = self.__json_serializer.encode_playing_as(color)
        self.__send_message(msg)

    def notify_opponent_colors(self, colors):
        """ Implements PlayerInterface.notify_opponent_colors() """
        msg = self.__json_serializer.encode_playing_with(colors)
        self.__send_message(msg)

    def tournament_has_started(self) -> bool:
        """ Implements PlayerInterface.tournament_has_started() """
        msg = self.__json_serializer.encode_tournament_start(True)
        self.__send_message(msg)
        return True

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    @property
    def socket(self):
        return self.__socket

    @property
    def color(self):
        return self.__color