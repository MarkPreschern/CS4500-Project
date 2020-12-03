import sys
import unittest
import socket
import threading
import time
import random
from unittest.mock import patch

sys.path.append('Common/')
sys.path.append('Remote/')

from server import Server
from client import Client
from remote_player_proxy import RemotePlayerProxy


class ServerTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ServerTests, self).__init__(*args, **kwargs)

        self.host = 'localhost'
        self.port = 3000

    def server_thread_func(self, server, port):
        server.run(port)

    def client_thread_func(self, to_send):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, self.port))
        client.sendall(to_send)
        client.close()

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

    # Server can successfully sign up one player
    def test_signs_up_client(self):
        server = Server(signup_timeout=3)
        client = Client('test')
        s_thread = threading.Thread(target=self.server_thread_func, args=(server, self.port))
        s_thread.start()

        time.sleep(1)
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, self.port))
        client.sendall('my name'.encode('ascii'))
        client.close()

        s_thread.join()
        self.assertEquals(len(server._remote_player_proxies), 1)

    # Server does not accept non-ascii characters, empty name, or name length > 12 characters
    def test_invalid_names(self):
        server = Server(signup_timeout=3)

        s_thread = threading.Thread(target=self.server_thread_func, args=(server, self.port))
        s_thread.start()

        time.sleep(1)

        threads = []
        threads.append(threading.Thread(target=self.client_thread_func, args=('valid'.encode('ascii'),)))
        threads.append(threading.Thread(target=self.client_thread_func, args=(''.encode('ascii'),)))
        threads.append(threading.Thread(target=self.client_thread_func, args=('test test test test test'.encode('ascii'),)))
        threads.append(threading.Thread(target=self.client_thread_func, args=('Á'.encode('utf-8'),)))
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        s_thread.join()

        self.assertEquals(len(server._remote_player_proxies), 1)

    # Test server does not sign up two players with the same name
    def test_duplicate_names(self):
        server = Server(signup_timeout=3)

        s_thread = threading.Thread(target=self.server_thread_func, args=(server, self.port))
        s_thread.start()

        time.sleep(1)

        threads = []
        threads.append(threading.Thread(target=self.client_thread_func, args=('A'.encode('ascii'),)))
        threads.append(threading.Thread(target=self.client_thread_func, args=('X'.encode('ascii'),)))
        threads.append(threading.Thread(target=self.client_thread_func, args=('X'.encode('ascii'),)))
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        s_thread.join()

        self.assertEquals(len(server._remote_player_proxies), 3)

    # Test tournament will start with enough players
    def test_tournament_will_start(self):
        server = Server(signup_timeout=3)

        s_thread = threading.Thread(target=self.server_thread_func, args=(server, self.port))
        s_thread.start()

        time.sleep(1)
        
        with patch.object(server, '_run_tournament', return_value=[]) as mock:

            client_names = ['A', 'B', 'C', 'D', 'E']
            threads = []

            for name in client_names:
                threads.append(threading.Thread(target=self.client_thread_func, args=(name.encode('ascii'),)))

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            s_thread.join()

            time.sleep(1)
            mock.assert_called_once
            self.assertEquals(len(server._remote_player_proxies), 5)
            self.assertEquals(server._signup_periods, 1)
    
    # Tournament does not start with < min players
    def test_not_enough_players(self):
        server = Server(signup_timeout=3)

        s_thread = threading.Thread(target=self.server_thread_func, args=(server, self.port))
        
        with patch.object(server, '_run_tournament', return_value = []) as mock:
            s_thread.start()

            time.sleep(1)

            threads = []
            threads.append(threading.Thread(target=self.client_thread_func, args=('A'.encode('ascii'),)))
            threads.append(threading.Thread(target=self.client_thread_func, args=('B'.encode('ascii'),)))
            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            s_thread.join()

            mock.assert_not_called
            self.assertEquals(len(server._remote_player_proxies), 2)
            self.assertEquals(server._signup_periods, 0)

    def test_can_tournament_run(self):
        # Dummy socket can be used because we aren't running the tournament
        self.dummy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rp1 = RemotePlayerProxy('a', 1.0, self.dummy_sock)
        self.rp2 = RemotePlayerProxy('b', 2.0, self.dummy_sock)
        self.rp3 = RemotePlayerProxy('c', 3.0, self.dummy_sock)
        self.rp4 = RemotePlayerProxy('d', 4.0, self.dummy_sock)

        server = Server()
        server._remote_player_proxies = [self.rp1, self.rp2, self.rp3, self.rp4]
        self.assertFalse(server._can_tournament_run())

        self.rp5 = RemotePlayerProxy('e', 5.0, self.dummy_sock)
        server._remote_player_proxies.append(self.rp5)
        self.assertTrue(server._can_tournament_run())
