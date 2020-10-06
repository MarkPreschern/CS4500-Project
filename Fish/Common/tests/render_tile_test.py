from tkinter import Tk, Label, mainloop, Frame
import sys

sys.path.append('../')

from Board import Board

# Make up window
_window = Tk()
_window.wm_title('Tile test')

# Make up frame within window
frame = Frame(_window, width=405, height=180)
# Set window to use gridview
frame.grid(row=0, column=0)

# Build board
b = Board.min_oft_and_holes(3, 1)
# Render board
b.render(frame)

# Run tk mainloop
_window.mainloop()
