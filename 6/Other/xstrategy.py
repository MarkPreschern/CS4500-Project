import json
import sys

sys.path.append("../Fish/Player")
sys.path.append("../4/Other")
sys.path.append("../5/Other")

from xstate import initialize_state, _get_next_position, _str_to_color
from xtree import _action_to_json
from strategy import Strategy


def xstrategy():
    # Initialize objects to read to
    input_obj = ""

    # Read from STDIN indefinitely until stream is closed
    for k in sys.stdin:
        input_obj += k

    # Load from read string
    json_list = json.loads(input_obj)

    # Get desired depth and state from json_list
    depth = json_list[0]
    state = json_list[1]

    # Find the first player in the json state
    first_player_color = _str_to_color(state['players'][0]['color'])

    # Load the json state into a State object
    initialized_state = initialize_state(state)

    # Check if the first player in the array is stuck and print false to STDOUT if so
    if first_player_color in initialized_state.stuck_players:
        print(json.dumps(False))
    else:
        # Compute the best action the first player can take given the current state and depth
        best_action = Strategy.get_best_action(initialized_state, depth)

        # Print the best action to STDOUT
        print(_action_to_json(best_action))
