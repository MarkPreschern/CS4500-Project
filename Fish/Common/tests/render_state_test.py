#!/usr/bin/python3

from tkinter import Tk, Frame
import sys

sys.path.append('../')

from Board import Board
from State import State
from Player import Player
from Color import Color


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
s = State(b, [Player(2, 'Bob', 20, Color.RED),
              Player(3, 'Larry', 20, Color.BLACK)])

s.place_avatar(0, (0, 0))
s.place_avatar(1, (1, 2))
s.place_avatar(2, (5, 3))
s.place_avatar(3, (5, 0))
s.place_avatar(4, (5, 2))

s.move_avatar(0, (3, 1))

s.render(frame)
# Run tk mainloop
_window.mainloop()
