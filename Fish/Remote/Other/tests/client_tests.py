import sys
import unittest
from unittest.mock import patch

sys.path.append('Common/')
sys.path.append('Remote/')

from server import Server
from client import Client
from remote_player_proxy import RemotePlayerProxy


class ClientTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ClientTests, self).__init__(*args, **kwargs)
        # TODO

    def test_init_fail1(self):
        # Tests failing init due to invalid name
        with self.assertRaises(TypeError):
            Client({'not a str': 'duh'})

    def test_init_fail2(self):
        # Tests failing init due to invalid lookahead_depth
        with self.assertRaises(TypeError):
            Client("name", "not an int")

    def test_init_fail3(self):
        # Tests failing init due to lookahead_depth being negative
        with self.assertRaises(ValueError):
            Client("name", -1)

    # TODO

