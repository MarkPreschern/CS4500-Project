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
b = Board.min_oft_and_holes(5, [(0, 0), (1, 1), (1, 0)])

# Build state
s = State(b, [Player(2, 'Bob', 20, Color.RED),
              Player(3, 'Larry', 20, Color.BLACK)])

s.place_avatar(2, (0, 0))
s.place_avatar(3, (1, 0))


s.render(frame)
# Run tk mainloop
_window.mainloop()
