import sys

sys.path.append("../Fish/Remote")
sys.path.append("../Fish/Admin")

from server import Server
from referee import Referee
from manager import Manager
from remote_player_proxy import RemotePlayerProxy

DEBUG = True


def xserver(port):
    if DEBUG:
        Server.DEBUG = True
        RemotePlayerProxy.DEBUG = True

    # player timeout needs to be at least 3 for some move actions
    Referee.PLAYER_TIMEOUT = 3

    # guarantees that there are no holes
    Referee.DIFFICULTY_FACTOR = 0

    # the number of fish on each tile on each game board in the server's tournament is set to 2
    Manager.FISH_NUMBER = 2

    fish_server = Server()

    # Port: 3000 by default
    fish_server.run(port)
