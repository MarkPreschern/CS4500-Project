#!/usr/bin/python

from Tkinter import *
import sys

from Hexagon import Hexagon


def show_usage():
    """
    Prints program usage to stdout.
    """
    print("usage: ./xgui positive-integer")


def render_hex(size):
    """
    Renders hexagon of the given size
    in a new window.

    :param size: size to render hexagon
    :return: None
    """
    root = Tk()
    Hexagon(root, size)
    root.mainloop()


def xgui():
    """
    Main program logic.
    """
    try:
        # Make sure the right # of parameters were passed
        if len(sys.argv) != 2:
            raise ValueError()

        # Try to parse argument as integer
        val = int(sys.argv[1])

        # Make sure value is positive
        if val <= 0:
            show_usage()
        else:
            render_hex(val)
    except (ValueError, IndexError):
        show_usage()

