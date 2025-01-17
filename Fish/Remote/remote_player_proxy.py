import socket
import sys

sys.path.append('../Fish/Common')

from state import State
from position import Position
from action import Action
from color import Color
from player_status import PlayerStatus
from player_interface import IPlayer
from Other.json_serializer import JsonSerializer


class RemotePlayerProxy(IPlayer):
    """
    PURPOSE: The purpose of the Remote Player Proxy is to allow for remote clients to connect to our servers and participate
    in games and tournaments of Fish, while our admin server can view them as simply any other player.  Therefore,
    this remote player proxy handles any abnormal conditions that may arise in the networked communications with the
    remote client.

    INTERPRETATION: The remote player proxy is an implementation of our IPlayer interface that allows
    for a remote player to participate in games and tournaments of Fish.  When the referee our tournament manager
    makes a call to this players functions (i.e. requesting a placement), the remote player proxy will encode
    this request into a JSON protocol (see JsonSerializer documentation), and send it along to the remote client
    (player) it represents.  The client, also knowing this protocol, is able to decode the JSON message, calculate its
    placement, and send it back over the socket to this RPP.  This RPP then informs the referee (or tournament manager)
    of the remote player's request

    A player fails under several circumstances. These include breaking the rules (cheating), raising an exception, and
    taking too long to communicate (timeout). In the event of any of these failure conditions, the player is kicked from
    the tournament and additionally communication between the server and client is disconnected. The timeout period is
    dictated by the server's 'CLIENT_TIMEOUT'. The player can timeout if they take too long to acknowledge a message,
    send a placement point, or a move action.

    DEFINITION(S):
    RPP          -> remote player proxy
    socket       -> the TCP socket that allows this RPP to communicate with the remote player it represents
    age          -> time in seconds (since epoch) noted when this player signed up with our server (we interpret
                    this as the players age, and lower aged players are allocated to games first and take turns first)
    """
    DEBUG = False

    def __init__(self, name: str, age: float, sock: socket.SocketType):
        """
        Initializes a remote player proxy with a name, age, and TCP client socket. Also
        initializes this players color to None (will be set when they enter their first game),
        and initializes a JSON serializer for the purpose of sending and receiving JSON messages
        from the remote player.

        :param name: name is a string that will act as a unique identifier of this player on the Fish servers
        :param age: see definitions above
        :param sock: the client TCP socket that will allow our server to communicate with this player
        """
        # Validate params
        if not isinstance(name, str):
            raise TypeError('Expected str for name')

        if not isinstance(age, float):
            raise TypeError('Expected float for age')

        if not isinstance(sock, socket.SocketType):
            raise TypeError('Expected socket for sock')

        if len(name) == 0 or len(name) > 12:
            raise ValueError('name must be between 1 and 12 characters inclusive')

        self.__name = name
        self.__age = age
        self.__socket = sock
        self.__color = None
        self.__state = None
        self.__json_serializer = JsonSerializer()

        self.__kicked = False

    @property
    def name(self):
        """ Retrieves player proxy name """
        return self.__name

    @property
    def age(self):
        """ Retrieves player proxy age """
        return self.__age

    @property
    def socket(self):
        """ Retrieves player proxy socket """
        return self.__socket

    @property
    def color(self):
        """ Retrieves player proxy color """
        return self.__color

    @property
    def kicked(self):
        """ Retrieves whether the player was kicked or not """
        return self.__kicked

    def get_placement(self, state: State) -> Position:
        """ Implements PlayerInterface.get_placement(State). """
        # Validate params
        if not isinstance(state, State):
            raise TypeError('Expected State for state!')

        msg = self.__json_serializer.encode_setup(state)
        self.__send_message(msg)

        position_msgs = self.__receive_messages()
        if len(position_msgs) > 0:
            position = self.__json_serializer.decode_position(position_msgs[0])
            return position
        else:
            return None

    def get_action(self, state: State) -> Action:
        """ Implements PlayerInterface.get_action(State). """
        # Validate params
        if not isinstance(state, State):
            raise TypeError('Expected State for state!')

        # get last actions since player's previous move
        # always sends [] as our server isn't required to implement the actions[] part of take-turn
        actions = []
        
        msg = self.__json_serializer.encode_take_turn(state, actions)
        self.__send_message(msg)

        take_turn_msgs = self.__receive_messages()
        
        if len(take_turn_msgs) > 0:
            action = self.__json_serializer.decode_action(take_turn_msgs[0])
            return action
        else:
            return None

    def kick(self, reason: str) -> None:
        """ Implements PlayerInterface.kick_player(str) """
        # Validate params
        if not isinstance(reason, str):
            raise TypeError('Expected str for state!')

        if RemotePlayerProxy.DEBUG:
            print(f'[{self.name}] was kicked for {reason}!')

        self.teardown()
        self.__kicked = True

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
        
        return True

    def set_color(self, color: Color) -> bool:
        """ Implements PlayerInterface.set_color() """
        self.__color = color
        msg = self.__json_serializer.encode_playing_as(color)
        self.__send_message(msg)

        ack = self.__receive_messages()
        return self.__is_ack(ack)

    def notify_opponent_colors(self, colors) -> bool:
        """ Implements PlayerInterface.notify_opponent_colors() """
        msg = self.__json_serializer.encode_playing_with(colors)
        self.__send_message(msg)

        ack = self.__receive_messages()
        return self.__is_ack(ack)

    def tournament_has_started(self) -> bool:
        """ Implements PlayerInterface.tournament_has_started() """
        msg = self.__json_serializer.encode_tournament_start(True)
        self.__send_message(msg)

        ack = self.__receive_messages()
        return self.__is_ack(ack)

    def tournament_has_ended(self, is_winner) -> bool:
        """ Implements PlayerInterface.tournament_has_started() """
        msg = self.__json_serializer.encode_tournament_end(is_winner)
        self.__send_message(msg)

        ack = self.__receive_messages()
        return self.__is_ack(ack)

    def teardown(self):
        """ closes the socket, terminating the connection between the server and client """
        if self.__socket:
            self.__socket.close()

    def __receive_messages(self) -> [str]:
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
                if RemotePlayerProxy.DEBUG:
                    print(f'Lost client {self.name} because: ', e)
                return []

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
            self.__socket.sendall(bytes(data, 'ascii'))
        except Exception as e:
            if RemotePlayerProxy.DEBUG:
                print(e)

    def __is_ack(self, ack) -> bool:
        """
        Returns True if the ack is properly formed, implying that the message received by the client was acknowledged,
        and returns False otherwise.

        :param ack: The supposed acknowledgement of a message, should be [['void']]
        :return: True if the message is acknowledged or False otherwise
        """
        return ack == ['void']
