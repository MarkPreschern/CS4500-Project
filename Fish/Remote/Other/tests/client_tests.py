import sys
import unittest
import socket
import threading
import time

sys.path.append('Common/')
sys.path.append('Remote/')

from client import Client
from json_serializer import JsonSerializer


class ClientTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ClientTests, self).__init__(*args, **kwargs)

        self.c1 = Client("a", 1)

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

        c_thread = threading.Thread(target=thread_func, args=(self.c1, self.host, self.port,))
        c_thread.start()

        client, address = self.server.accept()

        # send end tournament message
        msg = self.json_serializer.encode_tournament_end(False)
        client.sendall(bytes(msg, 'ascii'))

        self.__close_server()

        time.sleep(0.1)
        self.assertTrue(self.c1.is_tournament_over)
        self.assertFalse(self.c1.won_tournament)

    def test_run_won_tournament(self):
        # tests running a client who loses a tournament
        Client.NO_MESSAGE_TIMEOUT = 1
        self.__start_server()

        # run client on separate thread
        def thread_func(client1, host, port):
            client1.run(host, port)

        c_thread = threading.Thread(target=thread_func, args=(self.c1, self.host, self.port,))
        c_thread.start()

        client, address = self.server.accept()

        # send end tournament message
        msg = self.json_serializer.encode_tournament_end(True)
        client.sendall(bytes(msg, 'ascii'))

        self.__close_server()

        time.sleep(0.1)
        self.assertTrue(self.c1.is_tournament_over)
        self.assertTrue(self.c1.won_tournament)

    def test__teardown(self):
        self.__start_server()
        self.c1._Client__init_socket(self.host, self.port)
        self.c1._Client__teardown()
        self.assertFalse(self.c1.lost_connection)
        self.__close_server()

    def test_init_socket_failed_connection(self):
        # tests initializing a client socket with a failed connection
        self.c1._Client__init_socket(self.host, self.port)
        self.assertTrue(self.c1.lost_connection)

    def test_init_socket_success(self):
        # tests initializing a client socket
        self.__start_server()
        self.c1._Client__init_socket(self.host, self.port)
        self.c1._Client__teardown()
        self.assertFalse(self.c1.lost_connection)
        self.__close_server()

    def test_listen_for_messages(self):
        # tests a client listening for messages
        Client.NO_MESSAGE_TIMEOUT = 1
        self.__start_server()

        # run client on separate thread
        def thread_func(client1, host, port):
            client1._Client__init_socket(host, port)
            client1._Client__listen_for_messages()

        c_thread = threading.Thread(target=thread_func, args=(self.c1, self.host, self.port,))
        c_thread.start()

        client, address = self.server.accept()

        # send end tournament message
        msg = self.json_serializer.encode_tournament_end(True)
        client.sendall(bytes(msg, 'ascii'))

        self.__close_server()

        time.sleep(0.1)
        self.assertTrue(self.c1.is_tournament_over)
        self.assertTrue(self.c1.won_tournament)

    def test_listen_for_messages_lost_connection(self):
        # tests a client listening for messages but loses connection
        Client.NO_MESSAGE_TIMEOUT = 1
        self.__start_server()

        # run client on separate thread
        def thread_func(client1, host, port):
            client1._Client__init_socket(host, port)
            client1._Client__listen_for_messages()

        c_thread = threading.Thread(target=thread_func, args=(self.c1, self.host, self.port,))
        c_thread.start()

        self.__close_server()

        time.sleep(0.1)
        self.assertTrue(self.c1.lost_connection)

    def test_listen_for_messages_timeout(self):
        # tests a client listening for messages but times out
        Client.NO_MESSAGE_TIMEOUT = 0.1
        self.__start_server()

        # run client on separate thread
        def thread_func(client1, host, port):
            client1._Client__init_socket(host, port)
            client1._Client__listen_for_messages()

        c_thread = threading.Thread(target=thread_func, args=(self.c1, self.host, self.port,))
        c_thread.start()

        time.sleep(0.2)

        self.__close_server()
        self.assertTrue(self.c1.lost_connection)

    def test_receive_messages(self):
        # tests a client listening for messages
        Client.NO_MESSAGE_TIMEOUT = 1
        self.__start_server()

        # run client on separate thread
        def thread_func(client1, host, port, output):
            client1._Client__init_socket(host, port)
            output[0] = client1._Client__receive_messages()

        output = [None] * 1

        c_thread = threading.Thread(target=thread_func, args=(self.c1, self.host, self.port, output,))
        c_thread.start()

        client, address = self.server.accept()

        # send end tournament message
        msg = self.json_serializer.encode_tournament_end(True)
        client.sendall(bytes(msg, 'ascii'))

        time.sleep(.1)
        self.__close_server()
        self.c1._Client__teardown()

        self.assertEqual(output[0], [['end', [True]]])

    def test_receive_messages_invalid_message(self):
        # tests a client listening for messages given an invalid message
        Client.NO_MESSAGE_TIMEOUT = 1
        self.__start_server()

        # run client on separate thread
        def thread_func(client1, host, port, output):
            client1._Client__init_socket(host, port)
            output[0] = client1._Client__receive_messages()

        output = [None] * 1

        c_thread = threading.Thread(target=thread_func, args=(self.c1, self.host, self.port, output,))
        c_thread.start()

        client, address = self.server.accept()

        # send end tournament message
        msg = "not a good message"
        client.sendall(bytes(msg, 'ascii'))

        self.__close_server()
        self.c1._Client__teardown()

        self.assertEqual(output[0], None)

    def test_receive_messages_lost_connection(self):
        # tests a client listening for messages when losing the connection

        # run client on separate thread
        def thread_func(client1, host, port):
            client1._Client__init_socket(host, port)
            client1._Client__receive_messages()

        c_thread = threading.Thread(target=thread_func, args=(self.c1, self.host, self.port,))
        c_thread.start()

        time.sleep(.1)
        self.assertTrue(self.c1.lost_connection)

    def test_send_message(self):
        # tests a client listening for messages
        Client.NO_MESSAGE_TIMEOUT = 1
        self.__start_server()

        # run client on separate thread
        def thread_func(client1, host, port):
            client1._Client__init_socket(host, port)
            client1._Client__send_message("hi")

        c_thread = threading.Thread(target=thread_func, args=(self.c1, self.host, self.port,))
        c_thread.start()

        client, address = self.server.accept()

        # retrieve sent data from client
        data = client.recv(4096).decode('ascii')

        self.__close_server()
        self.c1._Client__teardown()

        self.assertEqual(data, "hi")

    def test_send_message_lost_connection(self):
        # tests a client listening for messages

        # run client on separate thread
        def thread_func(client1, host, port,):
            client1._Client__init_socket(host, port)
            client1._Client__send_message("hi")

        c_thread = threading.Thread(target=thread_func, args=(self.c1, self.host, self.port,))
        c_thread.start()

        time.sleep(.1)
        self.assertTrue(self.c1.lost_connection)
