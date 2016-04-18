#!/usr/bin/python
# Author: Alvin Lin (alvin.lin.dev@gmail.com)
# This is a class that facilitates the generation of a raster ppm image file.
# X increases down and y increases across.

from color import Color
from decorators import deprecated
from util import Util

HEADER = "P3 %d %d %d\n"

class Picture():

    def __init__(self, width, height, max_color_value=255):
        """
        Constructor for the Picture class.

        Parameters:
        filename: str, the name of the new image file
        width: int, the width of the image in pixels
        height: int, the height of the image in pixels
        max_color_value: int, the max color value of the ppm, defaults to 255
        """
        self.width = width
        self.height = height
        self.max_color_value = max_color_value
        self.grid = [[Color("#FFFFFF") for x in range(
            width)] for y in range(height)]

    def set_pixel(self, x, y, color, suppress_error=True):
        """
        Sets the specified pixel to the specified color.

        Parameters:
        x: int, the x coordinate of the pixel to set
        y: int, the y coordinate of the pixel to set
        color: Color, the RGB color to set the pixel to
        suppress_error: bool (optional), when set to True, will suppress the
            error if the point is out of bounds
        """
        if Util.in_bound(x, 0, self.height) and Util.in_bound(y, 0, self.width):
            self.grid[x][y] = color
        elif not suppress_error:
            raise TypeError("Invalid coordinate %d %d." % (x, y))

    @deprecated
    def map(self, function, section=None):
        """
        Applies the given function transformation to a section of the grid.

        Parameters:
        function: function, a callback function that is run on the pixels in
            the grid.
        section: list, opposite corners of a rectangular region
            in the grid to apply the function transformation to.
        """
        x_range = [0, self.width]
        y_range = [0, self.height]
        if section:
            x_range = [min(section[0][0], section[1][0]),
                       max(section[0][0], section[1][0])]
            y_range = [min(section[0][1], section[1][1]),
                       max(section[0][1], section[1][1])]
        for x in range(x_range[0], x_range[1]):
            for y in range(y_range[0], y_range[1]):
                self.grid[x][y] = function(
                    [x, y], [self.width, self.height], self.grid[x][y])

    def generate(self, filename):
        """
        Writes the internal raster to a ppm image file.

        Parameters:
        filename: str, the name of the image file, excluding the extension
        """
        with open("%s.ppm" % filename, "w") as picture:
            picture.write(HEADER % (
                self.width, self.height, self.max_color_value))
            for row in self.grid:
                for pixel in row:
                    for color in pixel:
                        picture.write("%d " % color)
