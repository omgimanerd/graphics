#!/usr/bin/python
# This is a class abstracting the Transformation and Picture classes into a
# general Drawing class.
# Author: Alvin Lin (alvin.lin.dev@gmail.com)

from matrix import *
from picture import *
from util import *

from math import pi
from os import system, remove

class Drawing():
  def __init__(self, width, height):
    """
    Constructors for a Drawing class.

    Parameters:
    filename: str, the name of the new image file
    width: int, the width of the image in pixels
    height: int, the height of the image in pixels
    """
    self.width = width
    self.height = height
    self.picture = Picture(width, height)

  def draw_point(self, x, y, color, suppress_error=True):
    """
    Draws a point on the picture.

    Parameters:
    x: int, the x coordinate of the point to draw
    y: int, the y coordinate of the point to draw
    color: Color, the color to draw the point
    suppress_error: bool (optional), when set to True, will suppress the
      error if the point is out of bounds
    """
    self.picture.set_pixel(x, y, color, suppress_error)

  def draw_line(self, x1, y1, x2, y2, color):
    """
    Uses the Bresenham line algorithm to draw a line.

    Parameters:
    x1: int, the x coordinate of one endpoint of the line
    y1: int, the y coordinate of one endpoint of the line
    x2: int, the x coordinate of the other endpoint of the line
    y2: int, the y coordinate of the other endpoint of the line
    color: Color, the color of the line
    """
    dx = x2 - x1
    dy = y2 - y1
    if dx + dy < 0:
      dx *= -1
      dy *= -1
      x1, x2 = x2, x1
      y1, y2 = y2, y1

    if dx == 0:
      while y1 <= y2:
        self.draw_point(x1, y1, color)
        y1 += 1
    elif dy == 0:
      while x1 <= x2:
        self.draw_point(x1, y2, color)
        x1 += 1
    elif dy < 0:
      d = 0
      while x1 <= x2:
        self.draw_point(x1, y1, color)
        if d > 0:
          y1 += -1
          d += -dx
        x1 += 1
        d += -dy
    elif dx < 0:
      d = 0
      while y1 <= y2:
        self.draw_point(x1, y1, color)
        if d > 0:
          x1 += -1
          d += -dy
        y1 += 1
        d += -dx
    elif dx > dy:
      d = 0
      while x1 <= x2:
        self.draw_point(x1, y1, color)
        if d > 0:
          y1 += 1
          d += -dx
        x1 += 1
        d += dy
    else:
      d = 0
      while y1 <= y2:
        self.draw_point(x1, y1, color)
        if d > 0:
          x1 += 1
          d += -dy
        y1 += 1
        d += dx

  def draw_matrix(self, matrix, color):
    """
    Draws the given matrix onto the internal raster.

    Parameters:
    matrix: EdgeMatrix, the matrix of lines to draw
    color: Color, the color to draw the matrix with
    """
    if not isinstance(matrix, EdgeMatrix):
      raise ValueError('%s is not an EdgeMatrix' % matrix)
    for edge in matrix.get_rounded():
      self.draw_line(edge[0][0], edge[0][1], edge[1][0], edge[1][1], color)

  def draw_circle(self, center_x, center_y, radius, color, step=100):
    """
    Draws a circle onto the internal raster.

    Parameters:
    center_x: int, the x coordinate of the center of the circle
    center_y: int, the y coordinate of the center of the circle
    radius: int, the radius of the circle
    color: Color, the color of the circle
    step: int (optional), the number of steps to use when drawing splines
      for the circle
    """
    self.draw_matrix(EdgeMatrix.get_circle_matrix(center_x, center_y, radius,
                                                  step), color)

  def display(self):
    """
    Displays the current state of the internal raster.
    """
    filename = '%s.ppm' % hash(self.picture)
    self.generate(filename)
    system('display %s' % filename)
    remove(filename)

  def generate(self, filename):
    """
    Generates the ppm raster image file.

    Parameters:
    filename: str, the name of the image file to generate
    """
    self.picture.generate(filename)
