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

b = Board.homogeneous(2, 7, 3)

# Build state
state = State(b, [PlayerEntity("Bob Ross", Color.RED),
                  PlayerEntity("Eric Khart", Color.WHITE),
                  PlayerEntity("Bob Ross", Color.BLACK),
                  PlayerEntity("Eric Khart", Color.BROWN),
                  ])


# Place a bunch of avatars
state.place_avatar(Color.RED, Position(0, 0))
state.place_avatar(Color.BLACK, Position(2, 0))
state.place_avatar(Color.BROWN, Position(5, 0))
state.place_avatar(Color.RED, Position(6, 1))
state.place_avatar(Color.WHITE, Position(6, 0))
state.place_avatar(Color.BLACK, Position(4, 0))
state.place_avatar(Color.BROWN, Position(3, 0))

# Move player 1 avatar
state.move_avatar(Position(0, 0), Position(1, 0))
state.remove_player(Color.RED)

print(state.stuck_players)
# Move player 2 avatar
# s.move_avatar(Position(4, 1), Position(3, 1))

state.render(frame)
# Run tk mainloop
_window.mainloop()
