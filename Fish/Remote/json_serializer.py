import json
import sys

sys.path.append('../Fish/Common')
sys.path.append('../4/Other')
sys.path.append('../C')

from xstate import initialize_state, _str_to_color, _state_to_json
from color import Color
from state import State
from position import Position
from xjson import JsonParser
from action import Action

class JsonSerializer(object):
    """
    INTERPRETATION: TODO.

    PURPOSE: TODO.

    DEFINITION(S): TODO.

    TODO: Add validity checks to decoding
    """
    def __init__(self):
        self.__json_parser = JsonParser()

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
        return Action(Position(int(src[0]), int(src[1])), Position(int(dest[0]), int(dest[1])))
        
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