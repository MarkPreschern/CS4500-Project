#!/usr/bin/python3

import sys

sys.path.append("../Fish/Remote")

from client import Client

client_a = Client('a')
client_b = Client('b')
client_c = Client('c')
client_d = Client('d')
client_e = Client('e')

client_a.run('localhost', 8080)
client_b.run('localhost', 8080)
client_c.run('localhost', 8080)
client_d.run('localhost', 8080)
client_e.run('localhost', 8080)