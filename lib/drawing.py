#!/usr/bin/python
# This is a class abstracting the Transformation and Picture classes into a
# general Drawing class.
# Author: Alvin Lin (alvin.lin.dev@gmail.com)

from matrix import *
from parametric import *
from picture import *
from util import *

from math import pi

class Drawing():
  def __init__(self, width, height):
    """
    Constructors for a Drawing class.

    Parameters:
    filename: string, the name of the new image file
    width: number, the width of the image in pixels
    height: number, the height of the image in pixels
    """
    self.width = width
    self.height = height
    self.picture = Picture(width, height)

  def draw_point(self, x, y, color, safe=True):
    """
    Draws a point on the picture.

    Parameters:
    x: number, the x coordinate of the point to draw
    y: number, the y coordinate of the point to draw
    color: Color, the color to draw the point
    """
    if safe:
      if Util.in_bound(x, 0, self.width) and Util.in_bound(y, 0, self.height):
        self.picture.set_pixel(x, y, color)
    else:
      self.picture.set_pixel(x, y, color)

  def draw_bresenham_line(self, x1, y1, x2, y2, color, safe=True):
    """
    Uses the Bresenham line algorithm to draw a line.

    Parameters:
    x1: number, the x coordinate of one endpoint of the line
    y1: number, the y coordinate of one endpoint of the line
    x2: number, the x coordinate of the other endpoint of the line
    y2: number, the y coordinate of the other endpoint of the line
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
        self.draw_point(x1, y1, color, safe=safe)
        y1 += 1
    elif dy == 0:
      while x1 <= x2:
        self.draw_point(x1, y2, color, safe=safe)
        x1 += 1
    elif dy < 0:
      d = 0
      while x1 <= x2:
        self.draw_point(x1, y1, color, safe=safe)
        if d > 0:
          y1 += -1
          d += -dx
        x1 += 1
        d += -dy
    elif dx < 0:
      d = 0
      while y1 <= y2:
        self.draw_point(x1, y1, color, safe=safe)
        if d > 0:
          x1 += -1
          d += -dy
        y1 += 1
        d += -dx
    elif dx > dy:
      d = 0
      while x1 <= x2:
        self.draw_point(x1, y1, color, safe=safe)
        if d > 0:
          y1 += 1
          d += -dx
        x1 += 1
        d += dy
    else:
      d = 0
      while y1 <= y2:
        self.draw_point(x1, y1, color, safe=safe)
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
      self.draw_bresenham_line(edge[0][0], edge[0][1],
                               edge[1][0], edge[1][1],
                               color)

  def draw_circle(self, center_x, center_y, radius, color, step=100):
    """
    Generates and draws a circle onto the internal raster.

    Parameters:
    center_x: number, the x coordinate of the center of the circle
    center_y: number, the y coordinate of the center of the circle
    radius: number, the radius of the circle
    color: Color, the color of the circle
    """
    edge_matrix = EdgeMatrix()
    parametric = Parametric.circle_parametric(center_x, center_y, radius)
    counter = 0
    increment = (2 * pi) / step
    while counter < 2 * pi:
      edge_matrix.add_edge(parametric.get_point(counter),
                           parametric.get_point(counter + increment))
      counter += increment
    self.draw_matrix(edge_matrix, color)

  def generate(self, filename):
    """
    Generates the ppm raster image file.
    """
    self.picture.generate(filename)
