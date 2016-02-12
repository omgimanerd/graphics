#!/usr/bin/python
# Author: Alvin Lin (alvin.lin.dev@gmail.com)
# This is a class that contains drawing transformations applied to the Picture
# class.

from util import Util

class Transformation():
  @staticmethod
  def line_lambda(a, b, c, line_color, thickness):
    """
    Returns a function that is applied to a grid of pixels to draw a line.
    
    Parameters:
    a: number, A in Ax + By + C = 0
    b: number, B in Ax + By + C = 0
    c: number, C in Ax + By + C = 0
    line_color: Color, the color of the line
    thickness: number, the thickness of the line in pixels

    Returns:
    function()
    """
    return lambda current, dimens, current_color: (
      line_color if Util.is_point_on_line(
        a, b, c, current[0], current[1], thickness / 2) else current_color
    )

  @staticmethod
  def circle_stroke_lambda(cx, cy, r, circle_color, thickness):
    """
    Returns a function that is applied to a grid of pixels to outline a circle.

    Parameters:
    cx: number, the x coordinate of the center of the circle
    cy: number, the y coordinate of the center of the circle
    r: number, the radius of the circle
    circle_color: Color, the color of the circle
    thickness: number, the thickness in pixels of the outline of the circle

    Returns:
    function()
    """
    return lambda current, dimens, current_color: (
      circle_color if Util.is_point_on_circle(
        cx, cy, r, current[0], current[1], thickness / 2) else current_color
    )

  @staticmethod
  def circle_fill_lambda(cx, cy, r, circle_color):
    """
    Returns a function that is applied to a grid of pixels to fill a circle.
  
    Parameters:
    cx: number, the x coordinate of the center of the circle
    cy: number, the y coordinate of the center of the circle
    r: number, the radius of the circle
    circle_color: Color, the color of the circle

    Returns:
    function()
    """
    return lambda current, dimens, current_color: (
      circle_color if Util.is_point_in_circle(
        cx, cy, r, current[0], current[1]) else current_color
    )
