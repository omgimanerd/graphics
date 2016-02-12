#!/usr/bin/python
# Author: Alvin Lin (alvin.lin.dev@gmail.com)
# This is a class that facilitates the generation of a raster ppm image file.

from color import Color
from util import Util

HEADER = "P3 %d %d %d\n"

class Picture():
  def __init__(self, filename, width, height,
               max_color_value=255):
    """
    Constructor for a Picture class.

    Parameters:
    filename: string, the name of the new image file
    width: number, the width of the image in pixels
    height: number, the height of the image in pixels
    max_color_value: number, the max color value of the ppm, defaults to 255
    """
    self.filename = filename
    self.width = width
    self.height = height
    self.max_color_value = max_color_value
    self.grid = [[Color("#FFFFFF") for x in range(width)] for y in range(height)]

  def set_pixel(self, x, y, color):
    """
    Sets the specified pixel to the specified color.

    Parameters:
    x: number, the x coordinate of the pixel to set
    y: number, the y coordinate of the pixel to set
    color: Color, the RGB color to set the pixel to

    Returns:
    None
    """
    if Util.in_bound(x, 0, self.width - 1) and Util.in_bound(
        y, 0, self.height - 1):
      # The internal raster is reversed because of the way Python lists work.
      self.grid[y][x] = color
    else:
      raise ValueError("Invalid coordinate.")

  def map(self, function, section=None):
    """
    Applies the given function transformation to a section of the grid.
    
    Parameters:
    function: function([currentX, currentY], [width, height],
                       [currentR, currentG, currentB]), a callback function
      that is run on the pixels in the grid.
    section: [[x1, y1], [x2, y2]], opposite corners of a rectangular region
      in the grid to apply the function transformation to.

    Returns:
    None
    """
    x_range = [0, self.width]
    y_range = [0, self.height]
    if section:
      x_range = [min(section[0][0], section[1][0]),
                 max(section[0][0], section[1][0])]
      y_range = [min(section[0][1], section[1][1]),
                 max(section[0][1], section[1][1])]

    for y in range(y_range[0], y_range[1]):
      for x in range(x_range[0], x_range[1]):
        # The internal raster is reversed because of the way Python lists work.
        self.grid[y][x] = function([x, y], [self.width, self.height],
                                   self.grid[y][x])
      
  def generate(self):
    """
    Turns the internal grid into a ppm raster image file and generates the file.

    Parameters:
    None

    Returns:
    None
    """
    with open(self.filename, "w") as picture:
      picture.write(HEADER % (self.width, self.height, self.max_color_value))
      for row in self.grid:
        for pixel in row:
          for color in pixel:
            picture.write("%d " % color)
