import sys
import unittest

sys.path.append("../Fish/Common")
sys.path.append("../5/Other")

from board import Board


class XStrategyTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(XStrategyTests, self).__init__(*args, **kwargs)

        Board.DISABLE_SPRITE_MANAGER = True