import sys
import unittest
from unittest.mock import patch

sys.path.append('Common/')
sys.path.append('Remote/')

from server import Server
from client import Client
from remote_player_proxy import RemotePlayerProxy


class RemotePlayerProxyTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(RemotePlayerProxyTests, self).__init__(*args, **kwargs)
        # TODO

    def test_init_fail1(self):
        # Tests failing init due to invalid name
        with self.assertRaises(TypeError):
            RemotePlayerProxy({'not a str': 'duh'})

    def test_init_fail2(self):
        # Tests failing init due to invalid age
        with self.assertRaises(TypeError):
            RemotePlayerProxy("name", "not a float")

    def test_init_fail3(self):
        # Tests failing init due to invalid socket
        with self.assertRaises(TypeError):
            RemotePlayerProxy("name", 10.0, ["not a socket"])

    # TODO

