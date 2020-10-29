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

b = Board.homogeneous(2, 4, 2)

# Build state
state = State(b, [Player(1, "Bob Ross", Color.RED),
              Player(2, "Eric Khart", Color.BROWN),
              Player(3, "Bob Ross", Color.WHITE),
              Player(4, "Eric Khart", Color.BLACK),
              ])

# Successful placement
state.place_avatar(1, Position(0, 0))
state.place_avatar(2, Position(0, 1))
state.place_avatar(3, Position(1, 0))
state.place_avatar(4, Position(1, 1))
state.place_avatar(1, Position(2, 0))
state.place_avatar(2, Position(2, 1))
state.place_avatar(3, Position(3, 0))
state.place_avatar(4, Position(3, 1))


# Move player 1 avatar
# s.move_avatar(Position(1, 0), Position(7, 3))
# Move player 2 avatar
# s.move_avatar(Position(4, 1), Position(3, 1))

state.render(frame)
# Run tk mainloop
_window.mainloop()
