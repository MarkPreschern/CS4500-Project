import sys
import unittest

sys.path.append('Common/')
sys.path.append('Remote/Other')
sys.path.append('Common/exceptions')

from unittest.mock import patch
from json_serializer import JsonSerializer
from color import Color
from state import State
from action import Action
from JsonDecodeException import JsonDecodeException

class JsonSerializerTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(JsonSerializerTests, self).__init__(*args, **kwargs)
        self.serializer = JsonSerializer()

    ### PARSING JSON TESTS
    def test_ill_formed_jsons(self):
        with self.assertRaises(JsonDecodeException):
            invalid1 = '[\naaaaaaa'.encode('ascii')
            result1 = self.serializer.bytes_to_jsons(invalid1)
        
        with self.assertRaises(JsonDecodeException):
            invalid2 = '{ test }'.encode('ascii')
            result2 = self.serializer.bytes_to_jsons(invalid2)

        with self.assertRaises(JsonDecodeException):
            invalid3 = '[1a]'.encode('ascii')
            result3 = self.serializer.bytes_to_jsons(invalid3)

        with self.assertRaises(JsonDecodeException):
            invalid4 = 'void'.encode('ascii')
            result4 = self.serializer.bytes_to_jsons(invalid4)

    def test_some_ill_formed_jsons(self):
        with self.assertRaises(JsonDecodeException):
            invalid1 = '["test"]{a}}'.encode('ascii')
            result1 = self.serializer.bytes_to_jsons(invalid1)

    def test_handle_void(self):
        void1 = '"void"'.encode('ascii')
        result = self.serializer.bytes_to_jsons(void1)
        self.assertEquals(['void'], result)

        void3 = '["test"]"void"'.encode('ascii')
        result = self.serializer.bytes_to_jsons(void3)
        self.assertEquals([['test'], 'void'], result)

        void4 = '"void"["test"]'.encode('ascii')
        result = self.serializer.bytes_to_jsons(void4)
        self.assertEquals(['void', ['test']], result)

    ### ENCODING TESTS
    def test_encode_tournament_start(self):
        msg = self.serializer.encode_tournament_start(True)
        self.assertEquals(msg, '["start", [true]]')
        msg = self.serializer.encode_tournament_start(False)
        self.assertEquals(msg, '["start", [false]]')

    def test_encode_tournament_end(self):
        msg = self.serializer.encode_tournament_end(True)
        self.assertEquals(msg, '["end", [true]]')
        msg = self.serializer.encode_tournament_end(False)
        self.assertEquals(msg, '["end", [false]]')

    def test_encode_playing_as(self):
        msg = self.serializer.encode_playing_as(Color.RED)
        self.assertEquals(msg, '["playing-as", ["red"]]')
        msg = self.serializer.encode_playing_as(Color.WHITE)
        self.assertEquals(msg, '["playing-as", ["white"]]')
        msg = self.serializer.encode_playing_as(Color.BROWN)
        self.assertEquals(msg, '["playing-as", ["brown"]]')
        msg = self.serializer.encode_playing_as(Color.BLACK)
        self.assertEquals(msg, '["playing-as", ["black"]]')
        
    def test_encode_playing_with(self):
        msg = self.serializer.encode_playing_with([Color.RED, Color.WHITE])
        self.assertEquals(msg, '["playing-with", ["red", "white"]]')

    ### DECODING TESTS
    def test_decode_tournament_start(self):
        (type, args) = self.serializer.decode_message(['start', [True]])
        self.assertEquals(type, 'start')
        self.assertEquals(args, [True])
        (type, args) = self.serializer.decode_message(['start', [False]])
        self.assertEquals(type, 'start')
        self.assertEquals(args, [False])
    
    def test_decode_playing_as(self):
        (type, args) = self.serializer.decode_message(['playing-as', ['red']])
        self.assertEquals(type, 'playing-as')
        self.assertEquals(args, [Color.RED])

    def test_decode_playing_with(self):
        (type, args) = self.serializer.decode_message(['playing-with', ['brown', 'black']])
        self.assertEquals(type, 'playing-with')
        self.assertEquals(args, [Color.BROWN, Color.BLACK])

    def test_decode_setup(self):
        (type, args) = self.serializer.decode_message(['setup', [{"board": [[2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2]], "players": [{"score": 0, "places": [], "color": "red"}, {"score": 0, "places": [], "color": "white"}, {"score": 0, "places": [], "color": "brown"}, {"score": 0, "places": [], "color": "black"}]}]])
        self.assertEquals(type, 'setup')
        self.assertTrue(isinstance(args[0], State))

    def test_decode_take_turn(self):
        (type, args) = self.serializer.decode_message(['take-turn', [{"board": [[2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2]], "players": [{"score": 0, "places": [], "color": "red"}, {"score": 0, "places": [], "color": "white"}, {"score": 0, "places": [], "color": "brown"}, {"score": 0, "places": [], "color": "black"}]}, [[[1, 2],[2, 3]], [[0, 1], [3, 4]]]]])
        self.assertEquals(type, 'take-turn')
        self.assertTrue(isinstance(args[0], State))
        self.assertTrue(isinstance(args[1][0], Action))

    def test_decode_tournament_start(self):
        (type, args) = self.serializer.decode_message(['end', [True]])
        self.assertEquals(type, 'end')
        self.assertEquals(args, [True])
        (type, args) = self.serializer.decode_message(['end', [False]])
        self.assertEquals(type, 'end')
        self.assertEquals(args, [False])

    ### VALIDATION ERRORS
    def test_invalid_messages(self):
        with self.assertRaises(JsonDecodeException):
            self.serializer.decode_message(['start', []])
        with self.assertRaises(JsonDecodeException):
            self.serializer.decode_message(['end', [1]])
        with self.assertRaises(JsonDecodeException):
            self.serializer.decode_message('error')
        with self.assertRaises(JsonDecodeException):
            self.serializer.decode_message(['take-turn', [{"board": [[2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2]], "players": [{"score": 0, "places": [], "color": "red"}, {"score": 0, "places": [], "color": "white"}, {"score": 0, "places": [], "color": "brown"}, {"score": 0, "places": [], "color": "black"}]}]])
        with self.assertRaises(JsonDecodeException):
            self.serializer.decode_message(['invalid-key', [True]])
        with self.assertRaises(JsonDecodeException):
            self.serializer.decode_message(['playing-as', ['red', 'white']])
