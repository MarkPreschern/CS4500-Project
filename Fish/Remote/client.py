import socket
import sys

sys.path.append('../Fish/Player')
sys.path.append('../C')

from json_serializer import JsonSerializer
from strategy import Strategy

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
        self.__json_serializer = JsonSerializer()
        self.__color = None
        self.__is_tournament_over = False

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


    def __handle_message(self, json):
        """ Handle a message from the remote player proxy and generate the proper response to send """
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
        """ Handle the tournament start message from the remote player proxy """
        return None

    def __handle_playing_as(self, args):
        """ Handle the playing as message from the remote player proxy """
        color = self.__json_serializer.decode_playing_as_args(args)
        print(f'[{self.name}] is playing as {color}')
        self.set_color(color)
        return None

    def __handle_playing_with(self, args):
        """ Handle the playing with message from the remote player proxy """
        # TODO: Do we need to do anything here?
        return None

    def __handle_setup(self, args):
        state = self.__json_serializer.decode_setup(args)
        print(f'[{self.name}] [{self.color}] is calculating placement...')
        position = Strategy.place_penguin(self.color, state)
        print(f'[{self.name} ({self.color})]  [SEND -> RPP] placement ~ {position}')
        return self.__json_serializer.encode_position(position)

    def __handle_take_turn(self, args):
        state = self.__json_serializer.decode_take_turn(args)
        print(f'[{self.name}] is calculating turn...')
        # TODO: don't hardcode strategy depth
        action = Strategy.get_best_action(state, 2)
        print(f'[{self.name}] [{self.color}] [SEND -> RPP] take-turn ~ {action[0]} -> {action[1]}')
        return self.__json_serializer.encode_action(action)

    def __handle_tournament_end(self, args):
        """ Handle the tournament end message from the remote player proxy """
        print(f'[{self.name}] [RECV <- RPP] Winner = {args[0]}')
        self.__is_tournament_over = True

    def __teardown(self):
        self.__client_sock.close()

    def __receive_messages(self) -> str:
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
        Creates a client TCP socket connected to the given host and port. If this fails, it returns None.
        """
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_sock.connect((host, port))
            client_sock.setblocking(0)
            client_sock.settimeout(10)
            return client_sock
        except Exception:
            return None

    @property
    def name(self):
        return self.__name

    @property
    def color(self):
        return self.__color

    def set_color(self, color):
        self.__color = color