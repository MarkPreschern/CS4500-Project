import sys
import unittest
import socket
from unittest.mock import patch

sys.path.append('Common/')
sys.path.append('Remote/')

from server import Server
from client import Client
from remote_player_proxy import RemotePlayerProxy


class RemotePlayerProxyTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(RemotePlayerProxyTests, self).__init__(*args, **kwargs)

        self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock5 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

    def test_init_fail4(self):
        # Tests failing init due to empty name
        with self.assertRaises(ValueError):
            RemotePlayerProxy("", 2.0, self.sock1)

    def test_init_fail5(self):
        # Tests failing init due to name that is too long
        with self.assertRaises(ValueError):
            RemotePlayerProxy("thisstringistoolong", 2.0, self.sock1)

    # TODO

