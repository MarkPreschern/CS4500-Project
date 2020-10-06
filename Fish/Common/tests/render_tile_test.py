from tkinter import Tk, Label, mainloop, Frame
import sys

sys.path.append('../')

from Board import Board

# Make up window
_window = Tk()

# Make up frame within window
frame = Frame(_window)
# Set window to use gridview
frame.grid(row=0, column=0)

# Build board
b = Board.min_oft_and_holes(2, 1)
# Render tile at position (0,0)
b.render_tile(frame, (0, 0))

# Run tk mainloop
_window.mainloop()
