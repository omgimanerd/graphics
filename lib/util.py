#!/usr/bin/python
# Author: Alvin Lin (alvin.lin.dev@gmail.com)
# This is a class that contains utility methods for the Drawing class.

import math

class Util():
  tau = 2 * math.pi
  epsilon = 0.1

  @staticmethod
  def in_bound(x, lower, upper):
    if lower > upper:
      tmp = lower
      lower = upper
      upper = tmp
    return x >= lower and x < upper

  @staticmethod
  def is_almost_equal(a, b, epsilon=1):
    return abs(a - b) <= epsilon

  @staticmethod
  def is_point_on_line(a, b, c, px, py, threshold=2):
    """
    Ax + By + C = 0
    This algorithm operates under the assumption that a and b will never both
    be zero.
    """
    return (abs(px * a + py * b + c) / math.sqrt(a * a + b * b)) <= threshold
    if a == 0:
      return abs((-c / b) - py) <= threshold
    elif b == 0:
      return abs((-c / a) - px) <= threshold

  @staticmethod
  def is_point_on_circle(cx, cy, r, px, py, threshold=2):
    return Util.is_almost_equal(
      Util.get_euclidean_distance(cx, cy, px, py), r, threshold)

  @staticmethod
  def is_point_in_circle(cx, cy, r, px, py):
    return Util.get_euclidean_distance(cx, cy, px, py) <= r

  @staticmethod
  def get_manhattan_distance(x1, y1, x2, y2):
    return abs(y2 - y1) + abs(x2 - x1)

  @staticmethod
  def get_euclidean_distance_sq(x1, y1, x2, y2):
    return ((x2 - x1) ** 2) + ((y2 - y1) ** 2)

  @staticmethod
  def get_euclidean_distance(x1, y1, x2, y2):
    return math.sqrt(Util.get_euclidean_distance_sq(x1, y1, x2, y2))

  @staticmethod
  def are_points_closer_than(x1, y1, x2, y2, d):
    return Util.get_euclidean_distance_sq(x1, y1, x2, y2) <= d ** 2

if __name__ == "__main__":
  print Util.get_euclidean_distance(0, 0, 3, 4)
  print Util.is_point_on_line(-50, 0, 5000, 100, 101, 1)
