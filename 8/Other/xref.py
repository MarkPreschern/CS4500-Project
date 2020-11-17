import json
import sys

sys.path.append("../Fish/Player")
sys.path.append("../Fish/Admin")
sys.path.append("../Fish/")

from player import Player
from referee import Referee


def xref():
    # Initialize objects to read to
    input_obj = ""

    # Read from STDIN indefinitely until stream is closed
    for k in sys.stdin:
        input_obj += k

    # Load from read string
    json_obj = json.loads(input_obj)

    # Get rows, columns, players, and fish from json_obj
    rows = json_obj['row']
    columns = json_obj['column']
    fish = json_obj['fish']
    players = []

    # initialize players;
    for p in json_obj['players']:
        players.append(Player(p[0], p[1]))

    # Create Referee
    referee = Referee(rows, columns, players, fish)
    Referee.DIFFICULTY_FACTOR = 0

    # Run complete game
    referee.start()

    # Print referee winners
    print(map(lambda winner: winner.name(), referee.winners()))