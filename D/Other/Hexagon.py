from Tkinter import *
import matplotlib.path as mplPath
import numpy as np


class Hexagon(Frame):

    def __init__(self, root, size):
        Frame.__init__(self, None)

        self.__root = root
        self.__size = size
        self.__width = 3 * size
        self.__height = 2 * self.__size
        self.__padding = 1
        self.__drawHexagon()

    def __click_callback(self, event):
        """
        Handles click event.
        """
        self.__root.destroy()

    def __drawHexagon(self):
        """
        Render a hexagon on a empty canvas.
        """
        # Set title
        self.master.title("xgui")

        # Create canvas of appropriate size
        canvas = Canvas(self, width=self.__width + self.__padding,
                        height=self.__height + self.__padding)
        canvas.xview_moveto(self.__padding / 2.0)
        canvas.yview_moveto(self.__padding / 2.0)
        canvas.pack(fill=BOTH, expand=YES)

        # Add bottom line
        points = [self.__size, self.__size * 2,
                  self.__size * 2, self.__size * 2]
        # Add right side
        points += [self.__size * 3, self.__size, self.__size * 2, 0]
        # Add top side and left side slant
        points += [self.__size * 1, 0, 0, self.__size]

        # Draw polygon from points
        polygon = canvas.create_polygon(points, outline='#f11',
                                        fill='#ffffff', width=1)

        # Register click event for the polygon (hexagon)
        canvas.tag_bind(polygon, '<ButtonPress-1>', self.__click_callback)

        # Pack root
        self.pack(fill=BOTH, expand=YES)
