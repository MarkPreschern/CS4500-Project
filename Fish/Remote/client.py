import json
import socket
import sys
import time

sys.path.append('../Fish/Player')
sys.path.append('../C')

from Other.json_serializer import JsonSerializer
from strategy import Strategy


class Client(object):
    """
    PURPOSE: To connect to the Fish admin server at a specific hostname and port in order to play (remotely) in
    a tournament of Fish.

    INTERPRETATION: The client is a remote player whose logic can exist on a separate machine than our Fish
    admin servers, and still participate in a tournament of Fish.  It uses a TCP client socket (with a given
    hostname and port) to initiate a connection with the Fish admin servers, and then immediately send its name
    as an identifier.

    A client is able to handle various JSON messages from the server (i.e. tournament start / end,
    being given its color, responding to game states with its movement, etc.). Upon receiving a JSON message from the
    server, the client handles the message appropriately and sends back a response. In the event of a 'setup' or
    'take-turn' message being received, the client will send back the corresponding penguin placement or move action.
    For all other message types received, the client will return the string 'void' which serves as an acknowledgement
    of the message for the server.

    The client continues to listen for messages from the server until it receives a 'end' type message from the server
    indicating that the tournament has ended. Additionally, if the client loses connection to the server for whatever
    reason (including if the client is kicked from the tournament, in which the server closes its connection to the
    client) then it will no longer listen for messages. Once the client stops listening for messages, it is closed.

    DEFINITION(S):
    Name                      -> unique identifier for this player
    JSON Serializer           -> our component that is used in order to both encode and decode messages into the desired
                                 protocol format (i.e. JSON state -> Game State) (before being sent over the TCP socket)
    Color                     -> the client's color for the game of Fish they are currently in (this will change
                                 throughout the duration of the tournament)
    Remote player proxy (RPP) -> The player on the server side that is representing this remote player, and deals with
                                 the networked communication between this player and the Admins of the Fish server.
    actions                   -> An array of Actions represents the penguin moves since the last time this player called
                                 get_action It is empty if this is the first call or a player was eliminated since the
                                 last call.
    """
    DEBUG = False

    # large timeout because we want to client to be able to wait for tournament start after signing up
    NO_MESSAGE_TIMEOUT = 75
    CONNECTION_RETRIES = 10

    def __init__(self, name: str, lookahead_depth: int = 1):
        """
        Initializes a client with the given name, for the purpose of connecting to the Fish servers and playing
        in a tournament of fish.

        :param name: name is a string that will act as a unique identifier of this player on the Fish servers
        :param lookahead_depth: the number of turns to look ahead when employing our Maximin strategy for this player
        """
        # Validate params
        if not isinstance(name, str):
            raise TypeError('Expected str for name')

        if not isinstance(lookahead_depth, int):
            raise TypeError('Expected int for lookahead_depth')

        if lookahead_depth < 0:
            raise ValueError('lookahead_depth must be greater than zero')

        if len(name) == 0 or len(name) > 12:
            raise ValueError('name must be between 1 and 12 characters inclusive')

        self.__name = name
        self.__lookahead_depth = lookahead_depth
        self.__json_serializer = JsonSerializer()

        self.__client_socket = None
        self.__color = None
        self.__opponent_colors = None

        self.__lost_connection = False
        self.__is_tournament_over = False

        self.__won_tournament = False

    @property
    def name(self):
        """
        Retrieves client's age
        """
        return self.__name

    @property
    def color(self):
        """
        Retrieves client's color
        """
        return self.__color

    @property
    def opponent_colors(self):
        """
        Retrieves client's opponent's colors
        """
        return self.__opponent_colors

    @property
    def is_tournament_over(self):
        """
        Retrieves if the tournament is over
        """
        return self.__is_tournament_over

    @property
    def lost_connection(self):
        """
        Retrieves if the client lost connection
        """
        return self.__lost_connection

    @property
    def won_tournament(self):
        """
        Retrieves if the client won the tournament
        """
        return self.__won_tournament

    def run(self, host: str, port: int):
        """
        Connect to Fish servers and participate in a tournament of Fish.  This involves establishing an initial
        TCP connection with Fish servers, providing our player name, and then handling messages from server
        accordingly to allow us to play through sequential games of Fish in the tournament (and receive messaging
        about how we are performing).  This loop will terminate once the class variable (is_tournament_over) is set
        to True upon receiving a tournament_end message.

        :param host: The hostname of the server to connect to (Fish admin server)
        :param port: The port number of the server to connect to (Fish admin server)
        """
        # Initialize socket
        self.__client_socket = self.__init_socket(host, port)
        # if the socket is created successfully, continue
        if self.__client_socket:
            # sends client's name
            self.__client_socket.send(bytes(self.__name, 'ascii'))
            # while the tournament is ongoing, listen for messages and respond to them accordingly
            self.__listen_for_messages()
            # tears down the socket
            self.__teardown()

    def __init_socket(self, host: str, port: int) -> socket.SocketType:
        """
        Creates a client TCP socket connected to the given host and port, and return it.
        If this fails, it returns None.
        :return socket being initialized
        """

        retry_no = Client.CONNECTION_RETRIES
        while retry_no >= 0:
            if retry_no != Client.CONNECTION_RETRIES:
                # wait a bit before performing next attempt to see if the server will come back up, unless first try
                time.sleep(1)

            try:
                client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_sock.connect((host, port))
                client_sock.setblocking(0)
                client_sock.settimeout(self.NO_MESSAGE_TIMEOUT)
                if Client.DEBUG:
                    print("Connected to server successfully..")
                return client_sock 
            except socket.error as e:
                # error connecting to a socket
                if Client.DEBUG:
                    print(f'Connection failed, {retry_no} attempts left...')
                    print(e)
                retry_no -= 1
            except Exception as ex:
                print(ex)

        # if we failed to connect many times, lets shut down
        self.__lost_connection = True
        return None

    def __listen_for_messages(self):
        """
        While the tournament is ongoing, listen for messages being sent from the server (player proxy). Upon receiving
        messages, handle them and send a response accordingly.
        :return: None
        """

        while not (self.__is_tournament_over or self.__lost_connection):
            msgs = self.__receive_messages()
            if msgs is None or len(msgs) == 0:
                # Shutdown if we don't receive any messages in NO_MESSAGE_TIMEOUT seconds
                break
            for msg in msgs:
                if Client.DEBUG:
                    print(f'[{self.name}] [{self.color}] [RECV] <- [RPP]: {msg}')

                if msg:
                    res = self.__handle_message(msg)
                    if res:
                        self.__send_message(res)

    def __handle_message(self, json_msg: json) -> str:
        """ 
        Handle a message from the remote player proxy and generate the proper response to send. It will 
        pass the arguments of that message off to that message type's handler, and if a response is 
        required it will return that string response, else will return None.

        :param json_msg: the JSON message received through the connection to the Fish admin server
        :return: If a response is required, return the JSON string response, else 'void'
        """

        # Validate message format
        try:
            msg_type, decoded_args = self.__json_serializer.decode_message(json_msg)

            if msg_type == 'start':
                return self.__handle_tournament_start(decoded_args)
            elif msg_type == 'playing-as':
                return self.__handle_playing_as(decoded_args)
            elif msg_type == 'playing-with':
                return self.__handle_playing_with(decoded_args)
            elif msg_type == 'setup':
                return self.__handle_setup(decoded_args)
            elif msg_type == 'take-turn':
                return self.__handle_take_turn(decoded_args)
            elif msg_type == 'end':
                return self.__handle_tournament_end(decoded_args)
            else:
                return None
        except Exception:
            if Client.DEBUG:
                print('Client received invalid JSON message: ', json_msg)
            return None

    def __handle_tournament_start(self, args) -> str:
        """ 
        Handle the tournament start message from the remote player proxy.  Our current implementation
        does not benefit from handling this message.
        
        :param args: [Boolean] representing True if the tournament has started
        :return: a void string to acknowledge we received this message
        """
        is_starting = args[0]

        if not is_starting:
            self.__teardown()
        return json.dumps('void')

    def __handle_playing_as(self, args) -> str:
        """ 
        Handle the playing-as message from the remote player proxy
        
        :param args: [Color] representing the color that the player is represented as in the game that is starting
        :return: a void string to acknowledge we received this message
        """
        self.__color = args[0]

        if Client.DEBUG:
            print(f'[{self.name}] is playing as {self.__color}')

        return json.dumps('void')

    def __handle_playing_with(self, args):
        """ 
        Handle the playing-with message from the remote player proxy. Our current implementation does not
        benefit from handling this message.
        
        :param args: [Color, Color, ...] the array of colors representing the opponents in this player's current game
        :return: a void string to acknowledge we received this message
        """
        self.__opponent_colors = args
        return json.dumps('void')

    def __handle_setup(self, args):
        """
        Handle the setup message (request for placement) from the remote player proxy.
        
        :param args: [State] representing the current state of the game
        :return: the JSON-encoded Position message to send back to the RPP
        """
        state = args[0]

        if Client.DEBUG:
            print(f'[{self.name}] [{self.color}] is calculating placement...')

        position = Strategy.place_penguin(self.color, state)

        if Client.DEBUG:
            print(f'[{self.name} ({self.color})]  [SEND -> RPP] placement ~ {position}')

        return self.__json_serializer.encode_position(position)

    def __handle_take_turn(self, args):
        """
        Handle the take-turn message (request for turn movement) from the remote player proxy.
        
        :param args: [State] representing the current state of the game and [Action, ... , Action] representing either
                      an empty array or an array of Actions represents the penguin moves since the last time the
                      take-turn method was called. It is empty if this is the first call or a player was eliminated
                      since the last call.
        :return: the JSON-encoded Action message to send back to the RPP
        """
        state = args[0]

        if Client.DEBUG:
            print(f'[{self.name}] is calculating turn...')

        action = Strategy.get_best_action(state, self.__lookahead_depth)

        if Client.DEBUG:
            print(f'[{self.name}] [{self.color}] [SEND -> RPP] take-turn ~ {action[0]} -> {action[1]}')

        return self.__json_serializer.encode_action(action)

    def __handle_tournament_end(self, args):
        """
        Handle the tournament end message from the remote player proxy.

        :param args: [Boolean] representing whether this player won (true) or lost (false) the tournament
        :return: a void string to acknowledge we received this message
        """
        if Client.DEBUG:
            print(f'[{self.name}] [RECV <- RPP] Winner = {args[0]}')

        self.__is_tournament_over = True
        self.__won_tournament = args[0]
        return json.dumps('void')

    def __receive_messages(self):
        """ Receive message(s) from the remote player proxy and decode into a message JSON object(s) """
        while True:
            try:
                data = self.__client_socket.recv(4096)
                if data:
                    return self.__json_serializer.bytes_to_jsons(data)
            except socket.error as se:
                if Client.DEBUG:
                    print(f'Lost server because: ', se)
                self.__lost_connection = True
                return None
            except Exception as e:
                if Client.DEBUG:
                    print(f'Receive message error: ', e)
                return None

    def __send_message(self, msg: str):
        """ Send the given JSON message to the remote player proxy """
        try:
            self.__client_socket.sendall(bytes(msg, 'ascii'))
        except socket.error as se:
            if Client.DEBUG:
                print(f'Lost server because: ', se)
            self.__lost_connection = True
            return None
        except Exception as e:
            if Client.DEBUG:
                print(f'Send message error: ', e)
            return None

    def __teardown(self):
        """
        This method deals with closing the client TCP socket connection, and is called when we receive a
        message that the tournament is over (and break out of the main loop).
        """
        if self.__client_socket:
            self.__client_socket.close()
        if Client.DEBUG:
            print('** EXIT THREAD **')
