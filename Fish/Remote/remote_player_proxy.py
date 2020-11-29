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
        self.__color = None
        self.__json_serializer = JsonSerializer()

    def __receive_messages(self) -> str:
        """ Receive message(s) from the remote player proxy and decode into a message JSON object(s) """
        while True:
            try:
                data = self.__socket.recv(4096)
                if data:
                    msgs = self.__json_serializer.bytes_to_jsons(data)
                    for msg in msgs:
                        print(f'[RPP] [RECV] <- [{self.name}]: {msg}')
                    return msgs
            except Exception as e:
                print(e)
                return None

    def __send_message(self, data):
        """
        Send data through the socket connection.

        Note: This code was able to be reused from xtcp.py (Andrew Nedea, Mark Preschern 2020)

        :param sock: a socket object connected to a port
        :param data: the data to be sent
        """
        print(f'[RPP] [SEND] -> [{self.name}]: {data}')
        # Send all data from the JSON object and the JSON list
        try:
            self.__socket.sendall(bytes(data, 'utf-8'))
        except Exception as e:
            print(e)

    def get_placement(self, state: State) -> Position:
        """
        Implements PlayerInterface.get_placement(State).

        Throws InvalidGameStatus if we're past placement stage.
        Throws OutOfTilesException if no position are open.
        """
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
        """
        Implements PlayerInterface.get_action(State).

        Throws GameNotRunningException() if game is still in placement mode.
        """
        # Validate params
        if not isinstance(state, State):
            raise TypeError('Expected State for state!')

        msg = self.__json_serializer.encode_take_turn(state)
        self.__send_message(msg)

        take_turn_msgs = self.__receive_messages()
        action = self.__json_serializer.decode_take_turn_response(take_turn_msgs[0])
        return action

    def kick(self, reason: str) -> None:
        """
        Implements PlayerInterface.kick_player(str)
        """
        # Validate params
        if not isinstance(reason, str):
            raise TypeError('Expected str for state!')

        print(f'[{self.name}] was kicked for {reason}!')

    def sync(self, state: State) -> None:
        """
        Implements PlayerInterface.sync(State)
        """
        # Validate params
        if not isinstance(state, State):
            raise TypeError('Expected State for state!')

        # Update internal state
        self.__state = state
        # A real player may decide what to do with this information, but an A.I. will use
        # the state received via get_action and get_placement to decide on a response.

    def game_over(self, leaderboard: list, cheating_players: list, failing_players: list) -> None:
        """
        Implements PlayerInterface.game_over(dict, list, list).
        """
        # Validate params
        if not isinstance(leaderboard, list):
            raise TypeError('Expected list for leaderboard!')

        if not isinstance(cheating_players, list):
            raise TypeError('Expected list for cheating_players!')

        if not isinstance(failing_players, list):
            raise TypeError('Expected list for failing_players!')

        

    def status_update(self, status: PlayerStatus) -> bool:
        """
        Implements PlayerInterface.status_update(PlayerStatus)
        """
        if not isinstance(status, PlayerStatus):
            raise TypeError('Expected PlayerStatus for status!')

        print(status)
        
        if status == PlayerStatus.LOST_GAME:
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
        return True

    def notify_opponent_colors(self, colors):
        """ Implements PlayerInterface.notify_opponent_colors() """
        msg = self.__json_serializer.encode_playing_with(colors)
        self.__send_message(msg)
        return True

    def tournament_has_started(self) -> bool:
        """
        Implements PlayerInterface.tournament_has_started()
        """
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