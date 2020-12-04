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

        output = [None]

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

        output = [None]

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
        # tests a client sending a message but losing connection

        # run client on separate thread
        def thread_func(client1, host, port,):
            client1._Client__init_socket(host, port)
            client1._Client__send_message("hi")

        c_thread = threading.Thread(target=thread_func, args=(self.c1, self.host, self.port,))
        c_thread.start()

        time.sleep(.1)
        self.assertTrue(self.c1.lost_connection)

    def test_handle_message_invalid_json(self):
        # tests a client handling a message that is invalid json
        msg = "[invalid json"
        output = self.c1._Client__handle_message(msg)
        self.assertEqual(output, None)

    def test_handle_message_invalid_msg_type(self):
        # tests a client handling a message that is an invalid msg type
        msg = ['bad type', []]
        output = self.c1._Client__handle_message(msg)
        self.assertEqual(output, None)

    def test_handle_message_valid(self):
        # tests a client handling a valid message
        msg = ['start', [True]]
        output = self.c1._Client__handle_message(msg)
        self.assertEqual(output, '"void"')

    def test_handle_tournament_start_true(self):
        # tests a client handling a true tournament start message
        msg = [True]
        output = self.c1._Client__handle_tournament_start(msg)
        self.assertEqual(output, '"void"')

    def test_handle_tournament_start_false(self):
        # tests a client handling a false tournament start message
        Client.NO_MESSAGE_TIMEOUT = 1
        self.__start_server()
        
        output = [None]

        # run client on separate thread
        def thread_func(client1, host, port, output):
            client1._Client__init_socket(host, port)
            output[0] = client1._Client__handle_tournament_start([False])

        c_thread = threading.Thread(target=thread_func, args=(self.c1, self.host, self.port, output,))
        c_thread.start()

        self.server.accept()
        self.__close_server()

        time.sleep(0.1)
        self.assertEqual(output[0], '"void"')

    def test_handle_playing_as(self):
        # tests a client handling a playing_as message
        msg_type, msg = self.json_serializer.decode_message(['playing-as', ['brown']])
        output = self.c1._Client__handle_playing_as(msg)
        self.assertEqual(output, '"void"')

    def test_handle_playing_with(self):
        # tests a client handling a playing_with message
        msg_type, msg = self.json_serializer.decode_message(['playing-with', ['brown', 'red']])
        output = self.c1._Client__handle_playing_with(msg)
        self.assertEqual(output, '"void"')

    def test_handle_setup1(self):
        # tests a client handling a setup (penguin placement) message
        msg_type1, msg1 = self.json_serializer.decode_message(['playing-as', ['brown']])
        self.c1._Client__handle_playing_as(msg1)
        msg_type2, msg2 = self.json_serializer.decode_message([
            "setup",
            [{"board": [[2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2]],
              "players": [{"score": 0, "places": [], "color": "red"},
                          {"score": 0, "places": [], "color": "white"},
                          {"score": 0, "places": [], "color": "brown"}]}]
        ])
        output = self.c1._Client__handle_setup(msg2)
        self.assertEqual(output, '[0, 0]')

    def test_handle_setup2(self):
        # tests a client handling a setup (penguin placement) message, different color and a hole on the board
        msg_type1, msg1 = self.json_serializer.decode_message(['playing-as', ['red']])
        self.c1._Client__handle_playing_as(msg1)
        msg_type2, msg2 = self.json_serializer.decode_message([
            "setup",
            [{"board": [[0, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2]],
              "players": [{"score": 0, "places": [], "color": "red"},
                          {"score": 0, "places": [], "color": "white"},
                          {"score": 0, "places": [], "color": "brown"}]}]
        ])
        output = self.c1._Client__handle_setup(msg2)
        self.assertEqual(output, '[0, 1]')

    def test_handle_setup3(self):
        # tests a client handling a setup (penguin placement) message, different color and 3 holes on the board
        msg_type1, msg1 = self.json_serializer.decode_message(['playing-as', ['white']])
        self.c1._Client__handle_playing_as(msg1)
        msg_type2, msg2 = self.json_serializer.decode_message([
            "setup",
            [{"board": [[0, 0, 0, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2]],
              "players": [{"score": 0, "places": [], "color": "red"},
                          {"score": 0, "places": [], "color": "white"},
                          {"score": 0, "places": [], "color": "brown"}]}]
        ])
        output = self.c1._Client__handle_setup(msg2)
        self.assertEqual(output, '[0, 3]')

    def test_handle_take_turn1(self):
        # tests a client handling a take turn (penguin move) message, beginning of game
        msg_type1, msg1 = self.json_serializer.decode_message(['playing-as', ['red']])
        self.c1._Client__handle_playing_as(msg1)
        msg_type, msg = self.json_serializer.decode_message([
            "take-turn",
            [{"board": [[2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2]],
              "players": [{"score": 0, "places": [[0, 0], [0, 3], [1, 1]], "color": "red"},
                          {"score": 0, "places": [[0, 1], [0, 4], [1, 2]], "color": "white"},
                          {"score": 0, "places": [[0, 2], [1, 0], [1, 3]], "color": "brown"}]},
             []]
        ])
        output = self.c1._Client__handle_setup(msg)
        self.assertEqual(output, '[1, 4]')

    def test_handle_take_turn2(self):
        # tests a client handling a take turn (penguin move) message, middle of game
        msg_type1, msg1 = self.json_serializer.decode_message(['playing-as', ['brown']])
        self.c1._Client__handle_playing_as(msg1)
        msg_type, msg = self.json_serializer.decode_message([
            "take-turn",
            [{"board": [[0, 0, 0, 0, 0], [0, 0, 0, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2]],
              "players": [{"score": 4, "places": [[2, 2], [3, 0], [1, 3]], "color": "brown"},
                          {"score": 6, "places": [[2, 0], [2, 3], [3, 1]], "color": "red"},
                          {"score": 6, "places": [[2, 1], [1, 4], [3, 2]], "color": "white"}]},
             []]
        ])
        output = self.c1._Client__handle_setup(msg)
        self.assertEqual(output, '[2, 4]')

    def test_handle_take_turn3(self):
        # tests a client handling a take turn (penguin move) message, almost end of game
        msg_type1, msg1 = self.json_serializer.decode_message(['playing-as', ['white']])
        self.c1._Client__handle_playing_as(msg1)
        msg_type, msg = self.json_serializer.decode_message([
            "take-turn",
            [{"board": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 2, 0, 0, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2]],
              "players": [{"score": 8, "places": [[2, 1], [3, 4], [3, 2]], "color": "white"},
                          {"score": 8, "places": [[4, 2], [3, 0], [2, 4]], "color": "brown"},
                          {"score": 10, "places": [[4, 0], [3, 3], [3, 1]], "color": "red"}]},
             []]
        ])
        output = self.c1._Client__handle_setup(msg)
        self.assertEqual(output, '[4, 1]')

    def test_handle_tournament_end_won(self):
        # tests a client handling a tournament end message where the client won
        output = self.c1._Client__handle_tournament_end([True])
        self.assertEqual(output, '"void"')
        self.assertTrue(self.c1.is_tournament_over)
        self.assertTrue(self.c1.won_tournament)

    def test_handle_tournament_end_lost(self):
        # tests a client handling a tournament end message where the client lost
        output = self.c1._Client__handle_tournament_end([False])
        self.assertEqual(output, '"void"')
        self.assertTrue(self.c1.is_tournament_over)
        self.assertFalse(self.c1.won_tournament)
