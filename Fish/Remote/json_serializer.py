import json
import sys

sys.path.append('../Fish/Common')
sys.path.append('../4/Other')

from xstate import initialize_state, _str_to_color, _state_to_json
from color import Color
from state import State
from position import Position
from action import Action

class JsonSerializer(object):
    """
    TODO Add description of how we deal with ill-formed or invalid JSON messages, once we do that

    INTERPRETATION: A utility class specialized in encoding our game-related information into a JSON
    message protocol, and subsequently decoding these JSON messages back into their Python representations.
    Specifically, this component can be used by either a remote player proxy (server side) or
    by a client for understanding and creating JSON messages to be sent over TCP sockets (messages are 
    described below in definitions).

    PURPOSE: The JSON serializer is a component that encompasses all of the functionality needed to go from
    our game representations to JSON representations (and back).  An example of this could be a remote player
    proxy encoding our current game state (as given by the Referee) into JSON before sending it over its
    TCP socket to the remote player it represents (and asking for a penguin placement position).  Our client
    could then also use this class to decode the JSON game state back to a Python game state that is 
    compatible to be used with our strategy component.  The same process will need to be followed when it decides
    on a Position, and sends it back to the RPP.

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

    def encode_tournament_start(self, is_starting: bool) -> str:
        msg = ['start', [is_starting]]
        return self.json_to_str(msg)

    def encode_tournament_end(self, did_win: bool) -> str:
        msg = ['end', [did_win]]
        return self.json_to_str(msg)

    def encode_playing_as(self, color: Color) -> str:
        msg = ['playing-as', [color.name.lower()]]
        return self.json_to_str(msg)

    def decode_playing_as_args(self, args) -> Color:
        """ Interpret list of one color (string) as Color enum """
        return _str_to_color(args[0])

    def encode_playing_with(self, colors) -> str:
        msg = ['playing-with', [color.name.lower() for color in colors]]
        return self.json_to_str(msg)

    def encode_setup(self, state) -> str:
        msg = ['setup', [_state_to_json(state)]]
        return self.json_to_str(msg)

    def decode_setup(self, args) -> State:
        return initialize_state(args[0])

    def decode_position(self, pos_arr) -> Position:
        return Position(pos_arr[0], pos_arr[1])
        
    def encode_position(self, position: Position) -> str:
        return json.dumps([position.x, position.y])

    def encode_take_turn(self, state) -> str:
        msg = ['take-turn', [_state_to_json(state)]]
        return self.json_to_str(msg)

    def decode_take_turn(self, args) -> State:
        return initialize_state(args[0])

    def decode_take_turn_response(self, args) -> Position:
        src = args[0]
        dest = args[1]
        return Action(Position(src[0], src[1]), Position(dest[0], dest[1]))
        
    def encode_action(self, action: Action) -> str:
        return json.dumps([action[0], action[1]])

    def bytes_to_jsons(self, data: bytes):
        jsons = []
        decoder = json.JSONDecoder()
        while(True):
            try:
                (json_val, cursor) = decoder.raw_decode(data.decode('utf-8'))
            except Exception as e:
                print(e)
                print('Could not convert from bytes to JSON messages.')
                break

            jsons.append(json_val)
            data = data[cursor:]
            if data == b'':
                break
        return jsons

    def str_to_json(self, json_string: str) -> dict:
        try:
            return json.loads(json_string)
        except ValueError:
            return None

    def json_to_str(self, json_obj: dict) -> str:
        try:
            return json.dumps(json_obj)
        except ValueError:
            return None