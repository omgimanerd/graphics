#!/usr/bin/python
# Author: Alvin Lin (alvin.lin.dev@gmail.com)
# This is a class abstracting the Transformation and Picture classes into a
# general Drawing class.

from picture import Picture
from transformation import Transformation

class Drawing():
  def __init__(self, name, width, height):
    """
    Constructors for a Drawing class.

    Parameters:
    filename: string, the name of the new image file
    width: number, the width of the image in pixels
    height: number, the height of the image in pixels
    """
    self.picture = Picture(name, width, height)
    
  def draw_point(self, x, y, color):
    """
    Draws a point on the picture.
    
    Parameters:
    x: number, the x coordinate of the point to draw
    y: number, the y coordinate of the point to draw
    color: Color, the color to draw the point

    Returns:
    None
    """
    self.picture.set_pixel(x, y, color)

  def draw_line(self, x1, y1, x2, y2, color, thickness):
    """
    Draws a line on the picture.
    
    Parameters:
    x1: number, the x coordinate of one endpoint of the line
    y1: number, the y coordinate of one endpoint of the line
    x2: number, the x coordinate of the other endpoint of the line
    y2: number, the y coordinate of the other endpoint of the line
    color: Color, the color of the line
    thickness: number, the thickness of the line in pixels

    Returns:
    None

    TODO: Fix
    """
    
    """
    Values for y = mx + b line formula.
    y = mx + b
    b = y - mx
    We hack around the slope to prevent division by zero.
    """
    m = float(y2 - y1) / float(x2 - x1 + 0.00000001)
    b = y2 - (m * x2)
    print m, b
    """
    Values for Ax + By + C = 0 line formula.
    A = delta Y
    B = - delta X
    C = - delta X times b
    """
    A = y2 - y1
    B = -(x2 - x1)
    C = B * b
    print A, B, C
    self.picture.map(Transformation.line_lambda(A, B, C, color, thickness),
                     section=[[x1, y1], [x2, y2]])

  def draw_bresenham_line(self, x1, y1, x2, y2, color):
    """
    Uses the Bresenham line algorithm to draw a line.

    Parameters:
    x1: number, the x coordinate of one endpoint of the line
    y1: number, the y coordinate of one endpoint of the line
    x2: number, the x coordinate of the other endpoint of the line
    y2: number, the y coordinate of the other endpoint of the line
    color: Color, the color of the line
    
    Returns:
    None
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

  def stroke_circle(self, cx, cy, r, color, thickness):
    """
    Draws a circle outline on the picture.

    Parameters:
    cx: number, the x coordinate of the center of the circle
    cy: number, the y coordinate of the center of the circle
    r: number, the radius of the circle in pixels
    color: Color, the color of the circle
    thickness: number, the thickness of the circle outline

    Returns:
    None
    """
    self.picture.map(Transformation.circle_stroke_lambda(
      cx, cy, r, color, thickness))

  def fill_circle(self, cx, cy, r, color):
    """
    Draws a filled circle on the picture.

    Parameters:
    cx: number, the x coordinate of the center of the circle
    cy: number, the y coordinate of the center of the circle
    r: number, the radius of the circle in pixels
    color: Color, the color of the circle
    
    Returns:
    None
    """
    self.picture.map(Transformation.circle_fill_lambda(cx, cy, r, color))

  def stroke_rect(self, x1, y1, x2, y2, color, thickness):
    """
    Draws a rectangular outline on the picture.
    
    Parameters:
    x1: number, the x coordinate of one corner of the rectangle
    y1: number, the y coordinate of one corner of the rectangle
    x2: number, the x coordinate of the opposite corner of the rectangle
    y2: number, the y coordinate of the opposite corner of the rectangle
    """
    self.draw_line(x1, y1, x2, y1, color, thickness)
    self.draw_line(x1, y1, x1, y2, color, thickness)
    self.draw_line(x2, y2, x2, y1, color, thickness)
    self.draw_line(x2, y2, x1, y2, color, thickness)

  def generate(self):
    """
    Generates the ppm raster image file.

    Parameters:
    None
    
    Returns:
    None
    """
    self.picture.generate()
