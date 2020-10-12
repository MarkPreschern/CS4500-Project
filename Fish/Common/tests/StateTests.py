import unittest
from State import State
from Player import Player


class StateTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(StateTests, self).__init__(*args, **kwargs)

    def init_test_fail1(self):
        # Tests constructor failing due to invalid board
        state = State(['hello', 'Buick'],
                      players=[Player(), Player(), Player()])
