import json
import sys

sys.path.append('../Fish/Common')
sys.path.append('../Fish/Common/exceptions')
sys.path.append('../4/Other')

from xstate import initialize_state, _str_to_color, _state_to_json
from color import Color
from state import State
from position import Position
from action import Action
from JsonDecodeException import JsonDecodeException


class JsonSerializer(object):
    """
    PURPOSE: The JSON serializer is a component that encompasses all of the functionality needed to go from
    our game representations to JSON representations (and back).  An example of this could be a remote player
    proxy encoding our current game state (as given by the Referee) into JSON before sending it over its
    TCP socket to the remote player it represents (and asking for a penguin placement position).  Our client
    could then also use this class to decode the JSON game state back to a Python game state that is
    compatible to be used with our strategy component.  The same process will need to be followed when it decides
    on a Position, and sends it back to the RPP.

    INTERPRETATION: A utility class specialized in encoding our game-related information into a JSON
    message protocol, and subsequently decoding these JSON messages back into their Python representations.
    Specifically, this component can be used by either a remote player proxy (server side) or
    by a client for understanding and creating JSON messages to be sent over TCP sockets (messages are
    described below in definitions).

    When attempting to decode messages received, we ensure that the data received is correctly formed. If the data
    received is ill-formed or invalid JSON according to the specified protocol then a 'JsonDecodeException' is raised.

    DEFINITION(S):
    encode -> go from Python representation to JSON string representation
    decode -> go from JSON string representation to Python representation

    MESSAGES:
    - start: ["start", [Boolean]] -> void (True value tells the player that the tournament is beginning)
    - playing-as: ["playing-as", [Color]] -> void (tells the player what color they are playing in their current game)
    - playing-with: ["playing-with", [Color, ...]] -> void (used to show who the player is playing against this game)
    - setup: ["setup", [State]] -> Position (requests a penguin placement from the player as calculated from the current game state)
    - take-turn: ["take-turn", [State, [Action, ..., Action]]] -> Action (requests a turn from the player as calculated
      from the current game state, player is also provided all moves since last take-turn call)
    - end: ["end", [Boolean]] -> void (tells the player that the tournament is over, True = won, False = lost)
    """
    DEBUG = False

    ### DECODING HELPERS (JSON -> INTERNAL REPR.) ###
    def decode_message(self, msg: json):
        """ 
        Validate this JSON message, return the type (string) if valid

        :return: tuple(type, args) containing string type and converted (decoded) arguments for this message
        """
        if not len(msg) == 2:
            raise JsonDecodeException('Expected JSON message array to have length 2 [type, args]')
        if not isinstance(msg[0], str):
            raise JsonDecodeException('Expected str for JSON message type!')
        if not isinstance(msg[1], list):
            raise JsonDecodeException('Expected list for args in JSON message.')

        type = msg[0]
        args = msg[1]

        if type == 'start' or type == 'end':
            if not len(args) == 1 or not isinstance(args[0], bool):
                raise JsonDecodeException('Invalid format for tournament start / end message.')
            return type, args

        elif type == 'playing-as':
            if not len(args) == 1 or not isinstance(args[0], str):
                raise JsonDecodeException('Invalid format for playing-as message.')
            return type, [_str_to_color(color) for color in args]

        elif type == 'playing-with':
            if not len(args) > 0 or not all(isinstance(color, str) for color in args):
                raise JsonDecodeException('Invalid format for playing-with message.')
            return type, [_str_to_color(color) for color in args]

        elif type == 'setup':
            if not len(args) == 1:
                raise JsonDecodeException('Invalid format for setup message.')
            return type, [initialize_state(args[0])]

        elif type == 'take-turn':
            if not len(args) == 2:
                raise JsonDecodeException('Invalid format for take-turn message.')
            return type, [initialize_state(args[0]), [self.decode_action(action) for action in args[1]]]
        else:
            raise JsonDecodeException('Unknown type of JSON message.')

    def decode_action(self, action: json) -> Action:
        if not len(action) == 2:
            raise JsonDecodeException('Tried to decode invalid action.')
        return Action(self.decode_position(action[0]), self.decode_position(action[1]))

    def decode_position(self, position: json) -> Position:
        if not isinstance(position, list) or not len(position) == 2:
            raise JsonDecodeException('Tried to decode invalid position.')
        return Position(position[0], position[1])

    ### ENCODING HELPERS (INTERNAL REPR. -> JSON) ###
    def encode_tournament_start(self, is_starting: bool) -> str:
        msg = ['start', [is_starting]]
        return json.dumps(msg)

    def encode_tournament_end(self, did_win: bool) -> str:
        msg = ['end', [did_win]]
        return json.dumps(msg)

    def encode_playing_as(self, color: Color) -> str:
        msg = ['playing-as', [color.name.lower()]]
        return json.dumps(msg)

    def encode_playing_with(self, colors: [Color]) -> str:
        msg = ['playing-with', [color.name.lower() for color in colors]]
        return json.dumps(msg)

    def encode_setup(self, state: State) -> str:
        msg = ['setup', [_state_to_json(state)]]
        return json.dumps(msg)

    def encode_position(self, position: Position) -> str:
        return json.dumps([position.x, position.y])

    def encode_action(self, action: Action) -> str:
        return json.dumps(self.action_to_json(action))

    def encode_take_turn(self, state: State, actions: [Action]) -> str:
        json_actions = [self.action_to_json(action) for action in actions]
        msg = ['take-turn', [_state_to_json(state), json_actions]]
        return json.dumps(msg)

    ### UTILS ###
    def bytes_to_jsons(self, data: bytes):
        """
        Takes in data in bytes form, and attempts to decode adjacent JSON values (from string) into an
        array of JSON values.  It will return this array of messages it decodes.  In the case
        of ill-formed JSON, it simply returns an empty array [].
        :param data: adjacent JSON values in bytes form
        :return: a list of JSON values (messages)
        """
        jsons = []
        decoder = json.JSONDecoder()
        while (True):
            try:
                decoded = data.decode('ascii')
                (json_val, cursor) = decoder.raw_decode(decoded)
                jsons.append(json_val)
                data = data[cursor:]
                if data == b'':
                    break
            except Exception as e:
                if JsonSerializer.DEBUG:
                    print(f'Failed to decode \'{data}\' because: ', e)
                raise JsonDecodeException('Failed to decode bytes to JSON!')
        return jsons

    def position_to_json(self, position: Position) -> json:
        return [position.x, position.y]

    def action_to_json(self, action: Action) -> json:
        return [self.position_to_json(action[0]), self.position_to_json(action[1])]
