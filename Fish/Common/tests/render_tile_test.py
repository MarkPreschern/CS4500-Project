#!/usr/bin/python3

from tkinter import Tk, Frame
import sys

sys.path.append('../')

from Board import Board

# Make up window
_window = Tk()
_window.wm_title('Tile test')

# Make up frame within window
frame = Frame(_window, width=505, height=400)
# Set window to use gridview
frame.grid(row=0, column=0)

# Build board
b = Board.min_oft_and_holes(5, [(0, 0), (1, 1), (1, 0)])
# Render board
b.render(frame)

# Run tk mainloop
_window.mainloop()
