import sys
import unittest
import socket
import threading
import time
from unittest.mock import patch

sys.path.append('Common/')
sys.path.append('Remote/')

from server import Server
from client import Client
from remote_player_proxy import RemotePlayerProxy
from json_serializer import JsonSerializer


class ClientTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ClientTests, self).__init__(*args, **kwargs)

        self.c1 = Client("a", 1)
        self.c2 = Client("b", 1)
        self.c3 = Client("c", 2)
        self.c4 = Client("d", 2)
        self.c5 = Client("e", 3)

        self.server = None
        self.host = "localhost"
        self.port = 3001

        self.json_serializer = JsonSerializer()

    def __start_server(self):
        # starts the server on self.port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

    def __close_server(self):
        # closes the server on self.port
        self.server.close()

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

    def test_init_fail4(self):
        # Tests failing init due to empty name
        with self.assertRaises(ValueError):
            Client("", 2)

    def test_init_fail5(self):
        # Tests failing init due to name that is too long
        with self.assertRaises(ValueError):
            Client("thisstringistoolong", 2)

    def test_run_failed_connection(self):
        # tests running a client with a failed connection
        self.c1.run(self.host, self.port)
        self.assertTrue(self.c1.lost_connection)

    def test_run_timeout(self):
        # tests running a client that times out after 1 second
        Client.NO_MESSAGE_TIMEOUT = 1
        self.__start_server()
        self.c1.run(self.host, self.port)
        self.__close_server()
        self.assertTrue(self.c1.lost_connection)

    def test_run_lost_tournament(self):
        # tests running a client who loses a tournament
        Client.NO_MESSAGE_TIMEOUT = 1
        self.__start_server()

        # run client on separate thread
        def thread_func(client1, host, port):
            client1.run(host, port)

        c_thread = threading.Thread(target=thread_func, args=(self.c2, self.host, self.port,))
        c_thread.start()

        client, address = self.server.accept()

        # send end tournament message
        msg = self.json_serializer.encode_tournament_end(False)
        client.sendall(bytes(msg, 'ascii'))

        self.__close_server()

        time.sleep(0.1)
        self.assertTrue(self.c2.is_tournament_over)
        self.assertFalse(self.c2.won_tournament)

    def test_run_won_tournament(self):
        # tests running a client who loses a tournament
        Client.NO_MESSAGE_TIMEOUT = 1
        self.__start_server()

        # run client on separate thread
        def thread_func(client1, host, port):
            client1.run(host, port)

        c_thread = threading.Thread(target=thread_func, args=(self.c3, self.host, self.port,))
        c_thread.start()

        client, address = self.server.accept()

        # send end tournament message
        msg = self.json_serializer.encode_tournament_end(True)
        client.sendall(bytes(msg, 'ascii'))

        self.__close_server()

        time.sleep(0.1)
        self.assertTrue(self.c3.is_tournament_over)
        self.assertTrue(self.c3.won_tournament)

