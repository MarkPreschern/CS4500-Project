#!/usr/bin/python3

from tkinter import Tk, Frame
import sys

from position import Position

sys.path.append('../')

from board import Board
from state import State
from player import Player
from color import Color


# Make up window
_window = Tk()
_window.wm_title('Game state')

# Make up frame within window
frame = Frame(_window, width=505, height=400)
# Set window to use gridview
frame.grid(row=0, column=0)

# Build board
b = Board.homogeneous(1, rows=10, cols=4)

# Build state
s = State(b, [Player(1, 'Bob', 20, Color.RED),
              Player(2, 'Larry', 30, Color.BLACK),
              Player(3, "Gary", 102, Color.WHITE)])

# Place all avatars
# Player 1 place
s.place_avatar(Position(4, 0))
# Player 2 place
s.place_avatar(Position(0, 1))
# Player 3 place
s.place_avatar(Position(2, 2))
# Player 1 place
s.place_avatar(Position(1, 0))
# Player 2 place
s.place_avatar(Position(2, 0))
# Player 3 place
s.place_avatar(Position(3, 2))
# Player 1 place
s.place_avatar(Position(1, 1))
# Player 2 place
s.place_avatar(Position(4, 1))
# Player 3 place
s.place_avatar(Position(3, 0))

# Move player 1 avatar
s.move_avatar(Position(1, 0), Position(7, 3))
# Move player 2 avatar
s.move_avatar(Position(4, 1), Position(3, 1))

s.render(frame)
# Run tk mainloop
_window.mainloop()
