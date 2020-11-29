import socket
import sys

sys.path.append('../Fish/Player')
sys.path.append('../C')

from json_serializer import JsonSerializer
from strategy import Strategy

class Client(object):
    """
    INTERPRETATION: The client is a remote player whose logic can exist on a seperate machine than our Fish
    admin servers, and still participate in a tournament of Fish.  It uses a TCP client socket (with a given
    hostname and port) to initiate a connection with the Fish admin servers, and then immediately send its name
    as an identifier.  It is able to handle various JSON messages from the server (i.e. tournament start / end,
    being given its color, responding to game states with its movement, etc.).

    PURPOSE: To connect to the Fish admin server at a specific hostname and port in order to play (remotely) in
    a tournament of Fish.

    DEFINITION(S):
    Name - unique identifier for this player
    JSON Serializer - our component that is used in order to both encode and decode messages into the desired
    protocol format (i.e. JSON state -> Game State) (before being sent over the TCP socket)
    Color - the client's color for the game of Fish they are currently in (this will change throughout the 
    duration of the tournament)
    Remote player proxy (RPP) - The player on the server side that is representing this remote player,
    and deals with the networked communication between this player and the Admins of the Fish server.
    """

    def __init__(self, name: str, lookahead_depth: int = 2):
        """
        Initializes a client with the given name, for the purpose of connecting to the Fish servers and playing
        in a tournament of fish.

        :param name: name is a string that will act as a unique identifier of this player on the Fish servers
        :param lookahead_depth: the number of turns to look ahead when employing our Maximin strategy for this player
        """
        self.__name = name
        self.__lookahead_depth = lookahead_depth
        self.__json_serializer = JsonSerializer()
        self.__color = None
        self.__is_tournament_over = False

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
        self.__client_sock = self.__init_socket(host, port)
        if self.__client_sock:
            self.__client_sock.send(bytes(self.__name, 'utf-8'))

            while not self.__is_tournament_over:
                msgs = self.__receive_messages()
                for msg in msgs:
                    print(f'[{self.name}] [{self.color}] [RECV] <- [RPP]: {msg}')
                    if msg:
                        res = self.__handle_message(msg)
                        if res:
                            self.__send_message(res)
            self.__teardown()
            print('** EXIT THREAD **')


    def __handle_message(self, json) -> str:
        """ 
        Handle a message from the remote player proxy and generate the proper response to send. It will 
        pass the arguments of that message off to that message type's handler, and if a response is 
        required it will return that string response, else will return None.

        :param json: the JSON message received through the connection to the Fish admin server
        :return: If a response is required, return the string response, else None
        """
        type = json[0]

        if type == 'start':
            self.__handle_tournament_start(json[1])
            return None
        elif type == 'playing-as':
            self.__handle_playing_as(json[1])
            return None
        elif type == 'playing-with':
            self.__handle_playing_with(json[1])
            return None
        elif type == 'setup':
            return self.__handle_setup(json[1])
        elif type == 'take-turn':
            return self.__handle_take_turn(json[1]) 
        elif type == 'end':
            self.__handle_tournament_end(json[1])
            return None
        else:
            return None

    def __handle_tournament_start(self, args):
        """ 
        Handle the tournament start message from the remote player proxy.  Our current implementation
        does not benefit from handling this message.
        
        :param args: [Boolean] representing True if the tournament has started
        """
        return None

    def __handle_playing_as(self, args):
        """ 
        Handle the playing-as message from the remote player proxy
        
        :param args: [Color] representing the color that the player is represented as in the game that is starting
        """
        color = self.__json_serializer.decode_playing_as_args(args)
        print(f'[{self.name}] is playing as {color}')
        self.set_color(color)
        return None

    def __handle_playing_with(self, args):
        """ 
        Handle the playing-with message from the remote player proxy. Our current implementation does not
        benefit from handling this message.
        
        :param args: [Color, Color, ...] the array of colors representing the opponents in this player's current game
        """
        return None

    def __handle_setup(self, args):
        """
        Handle the setup message (request for placement) from the remote player proxy.
        
        :param args: [State] representing the current state of the game
        :return: the JSON-encoded Position message to send back to the RPP
        """
        state = self.__json_serializer.decode_setup(args)
        print(f'[{self.name}] [{self.color}] is calculating placement...')
        position = Strategy.place_penguin(self.color, state)
        print(f'[{self.name} ({self.color})]  [SEND -> RPP] placement ~ {position}')
        return self.__json_serializer.encode_position(position)

    def __handle_take_turn(self, args):
        """
        Handle the take-turn message (request for turn movement) from the remote player proxy.
        
        :param args: [State] representing the current state of the game
        :return: the JSON-encoded Action message to send back to the RPP
        """
        state = self.__json_serializer.decode_take_turn(args)
        print(f'[{self.name}] is calculating turn...')
        action = Strategy.get_best_action(state, self.__lookahead_depth)
        print(f'[{self.name}] [{self.color}] [SEND -> RPP] take-turn ~ {action[0]} -> {action[1]}')
        return self.__json_serializer.encode_action(action)

    def __handle_tournament_end(self, args):
        """ 
        Handle the tournament end message from the remote player proxy.

        :param args: [Boolean] representing whether this player won (true) or lost (false) the tournament
        """
        print(f'[{self.name}] [RECV <- RPP] Winner = {args[0]}')
        self.__is_tournament_over = True

    def __teardown(self):
        """
        This method deals with closing the client TCP socket connection, and is called when we receive a
        message that the tournament is over (and break out of the main loop).
        """
        self.__client_sock.close()

    def __receive_messages(self):
        """ Receive message(s) from the remote player proxy and decode into a message JSON object(s) """
        while True:
            try:
                data = self.__client_sock.recv(4096)
                if data:
                    return self.__json_serializer.bytes_to_jsons(data)
            except Exception as e:
                print(e)
                return None

    def __send_message(self, msg: str):
        """ Send the given JSON message to the remote player proxy """
        try:
            self.__client_sock.sendall(bytes(msg, 'utf-8'))
        except Exception as e:
            print(e)
            return

    def __init_socket(self, host: str, port: int):
        """ 
        Creates a client TCP socket connected to the given host and port, and return it. 
        If this fails, it returns None.
        """
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_sock.connect((host, port))
            client_sock.setblocking(0)
            client_sock.settimeout(10)
            return client_sock
        except Exception:
            return None

    """ GETTERS AND SETTERS """
    @property
    def name(self):
        return self.__name

    @property
    def color(self):
        return self.__color

    def set_color(self, color):
        self.__color = color