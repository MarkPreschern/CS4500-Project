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
s = State(b, [Player(1, 'Bob', 20, Color.RED),
              Player(2, 'Larry', 30, Color.BLACK)])

# Player 1 place
s.place_avatar(0, (0, 0))
# Player 2 place
s.place_avatar(4, (5, 2))
# Player 1 place
s.place_avatar(1, (1, 2))
# Player 2 place
s.place_avatar(5, (6, 0))
# Player 1 place
s.place_avatar(2, (5, 3))
# Player 2 place
s.place_avatar(6, (7, 2))
# Player 1 place
s.place_avatar(3, (5, 0))
# Player 2 place
s.place_avatar(7, (8, 3))

# Move player 1 avatar
s.move_avatar(0, (3, 1))
# Move player 2 avatar
s.move_avatar(6, (8, 2))

s.render(frame)
# Run tk mainloop
_window.mainloop()
