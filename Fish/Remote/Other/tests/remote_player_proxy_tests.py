import sys
import unittest
import socket
import json
import threading
import time
from unittest import mock
from unittest.mock import patch

sys.path.append('Common/')
sys.path.append('Common/exceptions')
sys.path.append('Remote/')

from remote_player_proxy import RemotePlayerProxy
from player_entity import PlayerEntity
from board import Board
from color import Color
from state import State
from JsonDecodeException import JsonDecodeException
from position import Position
from action import Action
from xstate import _state_to_json
from player_status import PlayerStatus


class RemotePlayerProxyTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(RemotePlayerProxyTests, self).__init__(*args, **kwargs)
        self.port = 3003

        # Initialize some players for testing
        self.__p1 = PlayerEntity("John", Color.RED)
        self.__p2 = PlayerEntity("George", Color.WHITE)
        self.__p3 = PlayerEntity("Gary", Color.BLACK)
        self.__p4 = PlayerEntity("Jeanine", Color.BROWN)

        # Initialize board for testing
        self.__b = Board.homogeneous(5, 5, 3)

        # Initialize sockets for testing
        self.dummy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mock_socket = mock.Mock()
        self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

    def test_valid_json_invalid_message(self):
        # Tests that valid JSON but invalid message returns JsonDecodeException
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        rpp._RemotePlayerProxy__socket = self.mock_socket
        self.mock_socket.recv.return_value = b'["test"]'

        with self.assertRaises(JsonDecodeException):
            state = State(self.__b, players=[self.__p1, self.__p2, self.__p3])
            pos = rpp.get_placement(state)

    def test_invalid_json_placement(self):
        # Tests that receiving invalid JSON results in a None placement
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        rpp._RemotePlayerProxy__socket = self.mock_socket
        self.mock_socket.recv.return_value = b'['
        state = State(self.__b, players=[self.__p1, self.__p2, self.__p3])
        pos = rpp.get_placement(state)
        self.assertEqual(pos, None)

    def test_get_placement_success(self):
        # Test that RPP can successfully request, receive and decode a position
        # This is done to bypass the constructor type checking
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        rpp._RemotePlayerProxy__socket = self.mock_socket
        self.mock_socket.recv.return_value = b'[0, 1]'

        state = State(self.__b, players=[self.__p1, self.__p2, self.__p3])
        json_state = _state_to_json(state)

        expected_client_request = f'["setup", [{json.dumps(json_state)}]]'
        
        with patch.object(rpp, '_RemotePlayerProxy__send_message') as mock:
            pos = rpp.get_placement(state)
            mock.assert_called_with(expected_client_request)
            self.assertEqual(pos, Position(0, 1))

    def test_get_action_success(self):
        # Test that RPP can successfully request, receive, and decode an Action
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        rpp._RemotePlayerProxy__socket = self.mock_socket
        self.mock_socket.recv.return_value = b'[[0, 1], [2, 2]]'

        state = State(self.__b, players=[self.__p1, self.__p2, self.__p3])
        json_state = _state_to_json(state)

        expected_client_request = f'["take-turn", [{json.dumps(json_state)}, []]]'
        
        with patch.object(rpp, '_RemotePlayerProxy__send_message') as mock:
            action = rpp.get_action(state)
            mock.assert_called_with(expected_client_request)
            self.assertEqual(action, Action(Position(0, 1), Position(2, 2)))

    def test_get_action_returns_position(self):
        # Test that receiving a position when asking for an action throws JsonDecodeException and returns None
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        rpp._RemotePlayerProxy__socket = self.mock_socket
        self.mock_socket.recv.return_value = b'[0, 1]'

        state = State(self.__b, players=[self.__p1, self.__p2, self.__p3])
        json_state = _state_to_json(state)

        expected_client_request = f'["take-turn", [{json.dumps(json_state)}, []]]'
        
        with patch.object(rpp, '_RemotePlayerProxy__send_message') as mock:
            with self.assertRaises(JsonDecodeException):
                action = rpp.get_action(state)
                mock.assert_called_with(expected_client_request)
                self.assertEqual(action, None)

    def test_kick_success(self):
        # Test that kicking the player sets their internal state to kicked, and returns None
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        res = rpp.kick('test')
        self.assertTrue(rpp.kicked)
        self.assertEquals(res, None)

    def test_sync(self):
        # Tests that we simply return None for sync
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        state = State(self.__b, players=[self.__p1, self.__p2, self.__p3])
        res = rpp.sync(state)
        self.assertEquals(res, None)

    def test_game_over(self):
        # Test that we simply return None for game_over
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        res = rpp.game_over([], [], [])
        self.assertEquals(res, None)

    def test_status_update(self):
        # Test that we simply return True for status_update
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        res = rpp.status_update(PlayerStatus.DISCONTINUED)
        self.assertEquals(res, True)
        res = rpp.status_update(PlayerStatus.WON_GAME)
        self.assertEquals(res, True)

    def test_set_color_success(self):
        # Test that RPP can successfully send a color and receive ACK from client
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        rpp._RemotePlayerProxy__socket = self.mock_socket
        self.mock_socket.recv.return_value = b'"void"'
        expected_client_request = f'["playing-as", ["red"]]'
        
        with patch.object(rpp, '_RemotePlayerProxy__send_message') as mock:
            ack = rpp.set_color(Color.RED)
            mock.assert_called_with(expected_client_request)
            self.assertEqual(ack, True)

    def test_set_color_no_ack(self):
        # Test that RPP will return False if no ack received for set_color
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        rpp._RemotePlayerProxy__socket = self.mock_socket
        self.mock_socket.recv.return_value = b'[1, 2]'
        expected_client_request = f'["playing-as", ["white"]]'
        
        with patch.object(rpp, '_RemotePlayerProxy__send_message') as mock:
            ack = rpp.set_color(Color.WHITE)
            mock.assert_called_with(expected_client_request)
            self.assertEqual(ack, False)

    def test_playing_with_success(self):
        # Test that RPP can successfully send a color and receive ACK from client
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        rpp._RemotePlayerProxy__socket = self.mock_socket
        self.mock_socket.recv.return_value = b'"void"'
        expected_client_request = f'["playing-with", ["red", "brown"]]'
        
        with patch.object(rpp, '_RemotePlayerProxy__send_message') as mock:
            ack = rpp.notify_opponent_colors([Color.RED, Color.BROWN])
            mock.assert_called_with(expected_client_request)
            self.assertEqual(ack, True)

    def test_playing_with_no_ack(self):
        # Test that RPP will return False if no ack received for set_color
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        rpp._RemotePlayerProxy__socket = self.mock_socket
        self.mock_socket.recv.return_value = b'whoops'
        expected_client_request = f'["playing-with", ["white", "black"]]'
        
        with patch.object(rpp, '_RemotePlayerProxy__send_message') as mock:
            ack = rpp.notify_opponent_colors([Color.WHITE, Color.BLACK])
            mock.assert_called_with(expected_client_request)
            self.assertEqual(ack, False)

    def test_tournament_end_success(self):
        # Test that RPP can successfully send a tournament end message and recieve ack
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        rpp._RemotePlayerProxy__socket = self.mock_socket
        self.mock_socket.recv.return_value = b'"void"'
        expected_client_request = f'["end", [false]]'
        
        with patch.object(rpp, '_RemotePlayerProxy__send_message') as mock:
            ack = rpp.tournament_has_ended(False)
            mock.assert_called_with(expected_client_request)
            self.assertEqual(ack, True)

    def test_tournament_end_no_ack(self):
        # Test that RPP will return False if no ack received for tournament_end
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        rpp._RemotePlayerProxy__socket = self.mock_socket
        self.mock_socket.recv.return_value = b'["testing"]'
        expected_client_request = f'["end", [true]]'
        
        with patch.object(rpp, '_RemotePlayerProxy__send_message') as mock:
            ack = rpp.tournament_has_ended(True)
            mock.assert_called_with(expected_client_request)
            self.assertEqual(ack, False)

    def test_tournament_start_success(self):
        # Test that RPP can successfully send a tournament start message and recieve ack
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        rpp._RemotePlayerProxy__socket = self.mock_socket
        self.mock_socket.recv.return_value = b'"void"'
        expected_client_request = f'["start", [true]]'
        
        with patch.object(rpp, '_RemotePlayerProxy__send_message') as mock:
            ack = rpp.tournament_has_started()
            mock.assert_called_with(expected_client_request)
            self.assertEqual(ack, True)

    def test_tournament_start_no_ack(self):
        # Test that RPP will return False if no ack received for tournament_start
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        rpp._RemotePlayerProxy__socket = self.mock_socket
        self.mock_socket.recv.return_value = b'[][]'
        expected_client_request = f'["start", [true]]'
        
        with patch.object(rpp, '_RemotePlayerProxy__send_message') as mock:
            ack = rpp.tournament_has_started()
            mock.assert_called_with(expected_client_request)
            self.assertEqual(ack, False)

    def test_receive_messages_success(self):
        # Tests that a remote proxy player can successfully receive a message from a client
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind(("localhost", self.port))
        server_sock.listen()

        # run client on separate thread
        def thread_func(port):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("localhost", port))
            time.sleep(.1)
            sock.sendall(bytes('"void"', 'ascii'))
            if sock:
                sock.close()

        c_thread = threading.Thread(target=thread_func, args=(self.port,))
        c_thread.start()

        client, address = server_sock.accept()
        rpp = RemotePlayerProxy('name', 1.0, client)

        response = rpp._RemotePlayerProxy__receive_messages()

        # close sockets
        if server_sock:
            server_sock.close()
        if rpp._RemotePlayerProxy__socket:
            rpp._RemotePlayerProxy__socket.close()

        self.assertEqual(response, ['void'])

    def test_receive_messages_lost_connection(self):
        # Tests that a remote proxy player can successfully receive a message from a client
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        response = rpp._RemotePlayerProxy__receive_messages()
        self.assertEqual(response, [])

    def test_is_ack_true(self):
        # Tests a valid ack
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        is_ack = rpp._RemotePlayerProxy__is_ack(['void'])
        self.assertTrue(is_ack)

    def test_is_ack_false1(self):
        # Tests an invalid ack
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        is_ack = rpp._RemotePlayerProxy__is_ack('void')
        self.assertFalse(is_ack)

    def test_is_ack_false2(self):
        # Tests an invalid ack
        rpp = RemotePlayerProxy('name', 1.0, self.dummy_socket)
        is_ack = rpp._RemotePlayerProxy__is_ack([])
        self.assertFalse(is_ack)
