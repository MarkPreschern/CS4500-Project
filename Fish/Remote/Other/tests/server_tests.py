import sys
import unittest

sys.path.append('Common/')
sys.path.append('Remote/')

from unittest.mock import patch

from server import Server
from client import Client
from remote_player_proxy import RemotePlayerProxy

class ServerTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ServerTests, self).__init__(*args, **kwargs)
        self.rp1 = RemotePlayerProxy('a', 1, None)
        self.rp2 = RemotePlayerProxy('b', 2, None)
        self.rp3 = RemotePlayerProxy('c', 3, None)
        self.rp4 = RemotePlayerProxy('d', 4, None)
        self.rp5 = RemotePlayerProxy('e', 5, None)
        self.server = Server(signup_timeout=5, min_clients=2)

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

