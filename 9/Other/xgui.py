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
from game_visualizer import GameVisualizer


def xgui(args):
    Board.DISABLE_SPRITE_MANAGER = False

    # get specified player number
    player_no = int(args[1])

    # default player names
    player_names = ["a", "b", "c", "d"]

    # timeout parameters
    Referee.PLAYER_TIMEOUT = 60

    # creates players
    players = [Player(player_names[index]) for index in range(player_no)]

    # Create game visualizer
    game_visualizer = GameVisualizer(players)

    # run game visualization
    game_visualizer.run()
