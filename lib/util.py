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
      lower, upper = upper, lower
    return x >= lower and x < upper

  @staticmethod
  def is_almost_equal(a, b, epsilon=epsilon):
    return abs(a - b) <= epsilon

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
  print Util.is_almost_equal(1, 1.1)
