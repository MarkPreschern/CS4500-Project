#!/usr/bin/python3

import sys

sys.path.append("../Fish/Remote")

from server import Server

fish_server = Server()

fish_server.run(8080)