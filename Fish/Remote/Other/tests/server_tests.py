import sys
import unittest
import socket
from unittest.mock import patch

sys.path.append('Common/')
sys.path.append('Remote/')

from server import Server
from client import Client
from remote_player_proxy import RemotePlayerProxy


class ServerTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ServerTests, self).__init__(*args, **kwargs)

        self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock5 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.rp1 = RemotePlayerProxy('a', 1.0, self.sock1)
        self.rp2 = RemotePlayerProxy('b', 2.0, self.sock2)
        self.rp3 = RemotePlayerProxy('c', 3.0, self.sock3)
        self.rp4 = RemotePlayerProxy('d', 4.0, self.sock4)
        self.rp5 = RemotePlayerProxy('e', 5.0, self.sock5)
        self.server = Server(signup_timeout=5, min_clients=2)

    def test_init_fail1(self):
        # Tests failing init due to invalid signup_timeout
        with self.assertRaises(TypeError):
            Server({'not a int': 'duh'})

    def test_init_fail2(self):
        # Tests failing init due to invalid signup_timeout value
        with self.assertRaises(ValueError):
            Server(-1)

    def test_init_fail3(self):
        # Tests failing init due to invalid min_clients and max_clients
        with self.assertRaises(ValueError):
            Server(5, -1, -1, 5)

    def test_init_fail4(self):
        # Tests failing init due to invalid signup_periods
        with self.assertRaises(ValueError):
            Server(5, 5, 5, 0)

    def test_init_fail5(self):
        # Tests failing init due min_clients being greater than max_clients
        with self.assertRaises(ValueError):
            Server(5, 10, 5, 5)

    # Test server does not start with < min players

    # Test server does not start with > max players

    # Test server does another signup round if < min players

    # Test server does not sign up two players with the same name
    
    def test_is_name_available(self):
        self.server._remote_player_proxies = [self.rp1, self.rp2]
        self.assertTrue(self.server._is_name_available('c'))
        self.assertFalse(self.server._is_name_available('b'))

    def test_can_tournament_run(self):
        self.server._remote_player_proxies = [self.rp1, self.rp2, self.rp3, self.rp4]
        self.assertFalse(self.server._can_tournament_run())
        self.server._remote_player_proxies.append(self.rp5)
        self.assertTrue(self.server._can_tournament_run())

