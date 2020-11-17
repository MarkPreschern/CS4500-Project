import json
import sys

sys.path.append("../Fish/Player")
sys.path.append("../Fish/Admin")
sys.path.append("../Fish/Common")
sys.path.append("../Fish/Admin/Other")


from tile import Tile
from hole import Hole
from board import Board
from position import Position
from player_entity import PlayerEntity
from board import Board
from movement_direction import MovementDirection
from color import Color
from action import Action
from exceptions.InvalidActionException import InvalidActionException
from exceptions.GameNotRunningException import GameNotRunningException
from game_tree import GameTree
from position import Position
from state import State
from referee import Referee
from player import Player


def xref():
    Board.DISABLE_SPRITE_MANAGER = True

    # Initialize objects to read to
    input_obj = ''

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
        players.append(Player(name=p[0], search_depth=p[1]))

    # Create Referee
    Referee.DIFFICULTY_FACTOR = 0
    Referee.PLAYER_TIMEOUT = 60
    referee = Referee(rows, columns, players, fish)

    # Run complete game
    referee.start()

    # Print referee winners
    output_str = json.dumps(sorted([winner.name for winner in referee.winners]))
    print(output_str)
