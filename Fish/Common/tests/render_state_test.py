#!/usr/bin/python3

from tkinter import Tk, Frame
import sys

sys.path.append('../')

from board import Board
from state import State
from player import Player
from color import Color
from hole import Hole
from position import Position
from tile import Tile

# Make up window
_window = Tk()
_window.wm_title('Game state')

# Make up frame within window
frame = Frame(_window, width=505, height=400)
# Set window to use gridview
frame.grid(row=0, column=0)

# Build board
# b = Board.homogeneous(1, rows=10, cols=4)

b = Board({
            Position(0, 0): Tile(5),
            Position(0, 1): Tile(3),
            Position(0, 2): Tile(2),
            Position(1, 0): Tile(2),
            Position(1, 1): Tile(3),
            Position(1, 2): Tile(2),
            Position(2, 0): Tile(3),
            Position(2, 1): Tile(4),
            Position(2, 2): Tile(1),
            Position(3, 0): Tile(1),
            Position(3, 1): Tile(1),
            Position(3, 2): Tile(5),
            Position(4, 0): Tile(2),
            Position(4, 1): Tile(3),
            Position(4, 2): Tile(4)
        })

# Build state
s = State(b, [Player(9, "Bob Ross", 48, Color.RED),
              Player(10, "Eric Khart", 52, Color.BROWN),
              Player(11, "Ionut", 54, Color.BLACK),
              ])

# Player 1
s.place_avatar(Position(2, 0))
# Player 2
s.place_avatar(Position(0, 1))
# Player 3
s.place_avatar(Position(0, 2))
# Player 1
s.place_avatar(Position(1, 0))
# Player 2
s.place_avatar(Position(1, 2))
# Player 3
s.place_avatar(Position(0, 0))
# Player 1
s.place_avatar(Position(3, 1))
# Player 2
s.place_avatar(Position(2, 1))
# Player 3
s.place_avatar(Position(3, 2))

# Move player 1 avatar
# s.move_avatar(Position(1, 0), Position(7, 3))
# Move player 2 avatar
# s.move_avatar(Position(4, 1), Position(3, 1))

s.render(frame)
# Run tk mainloop
_window.mainloop()
