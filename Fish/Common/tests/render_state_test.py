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
    Position(0, 0): Tile(1),
    Position(0, 1): Tile(2),
    Position(0, 2): Tile(1),
    Position(0, 3): Tile(1),
    Position(0, 4): Tile(1),

    Position(1, 0): Tile(1),
    Position(1, 1): Tile(1),
    Position(1, 2): Tile(1),
    Position(1, 3): Tile(1),
    Position(1, 4): Tile(5),

    Position(2, 0): Tile(3),
    Position(2, 1): Tile(2),
    Position(2, 2): Tile(1),
    Position(2, 3): Tile(1),
    Position(2, 4): Tile(1),

    Position(3, 0): Tile(1),
    Position(3, 1): Tile(3),
    Position(3, 2): Tile(2),
    Position(3, 3): Tile(1),
    Position(3, 4): Tile(1)
})

# Build state
state = State(b, [Player("Bob Ross", Color.RED),
              Player("Eric Khart", Color.BROWN),
              Player("Bob Ross", Color.WHITE),
              Player("Eric Khart", Color.BLACK),
              ])

# Successful placement
state.place_avatar(Color.RED, Position(2, 1))
state.place_avatar(Color.BROWN, Position(0, 0))
state.place_avatar(Color.WHITE, Position(0, 1))
state.place_avatar(Color.BLACK, Position(1, 0))
state.place_avatar(Color.RED, Position(0, 2))
state.place_avatar(Color.BROWN, Position(2, 0))
state.place_avatar(Color.WHITE, Position(3, 1))
state.place_avatar(Color.BLACK, Position(3, 0))


# Move player 1 avatar
state.move_avatar(Position(2, 1), Position(1, 1))
# Move player 2 avatar
# s.move_avatar(Position(4, 1), Position(3, 1))

state.render(frame)
# Run tk mainloop
_window.mainloop()
