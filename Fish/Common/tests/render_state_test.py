#!/usr/bin/python3

from tkinter import Tk, Frame
import sys

sys.path.append('../')

from board import Board
from state import State
from player_entity import PlayerEntity
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

b = Board.homogeneous(3, 5, 3)

# Build state
state = State(b, [PlayerEntity("John", Color.RED),
                  PlayerEntity("Johnny", Color.WHITE)
                  ])


# Place a bunch of avatars
state.place_avatar(Color.RED, Position(0, 0))
state.place_avatar(Color.WHITE, Position(0, 1))

state.place_avatar(Color.RED, Position(0, 2))
state.place_avatar(Color.WHITE, Position(1, 0))

state.place_avatar(Color.RED, Position(1, 1))
state.place_avatar(Color.WHITE, Position(1, 2))

state.place_avatar(Color.RED, Position(2, 0))
state.place_avatar(Color.WHITE, Position(2, 1))
# Move player 1 avatar
# state.move_avatar(Position(2, 1), Position(1, 1))
# Move player 2 avatar
# s.move_avatar(Position(4, 1), Position(3, 1))

state.render(frame)
# Run tk mainloop
_window.mainloop()
