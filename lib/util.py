#!/usr/bin/python
# Author: Alvin Lin (alvin.lin.dev@gmail.com)
# This is a class that contains utility methods for the Drawing class.

import math

class Util():
  tau = 2 * math.pi
  epsilon = 0.1

  @staticmethod
  def in_bound(t, lower, upper):
    if lower > upper:
      lower, upper = upper, lower
    return t >= lower and t < upper

  @staticmethod
  def is_almost_equal(a, b, epsilon=epsilon):
    return abs(a - b) <= epsilon

  @staticmethod
  def get_manhattan_distance(t1, y1, t2, y2):
    return abs(y2 - y1) + abs(t2 - t1)

  @staticmethod
  def get_euclidean_distance_sq(t1, y1, t2, y2):
    return ((t2 - t1) ** 2) + ((y2 - y1) ** 2)

  @staticmethod
  def get_euclidean_distance(t1, y1, t2, y2):
    return math.sqrt(Util.get_euclidean_distance_sq(t1, y1, t2, y2))

  @staticmethod
  def are_points_closer_than(t1, y1, t2, y2, d):
    return Util.get_euclidean_distance_sq(t1, y1, t2, y2) <= d ** 2

  @staticmethod
  def get_hermite_function(a, b, c, d):
    return lambda t: (a * (t ** 3)) + (b * (t ** 2)) + (c * t) + d

  @staticmethod
  def get_bezier_function(a, b, c, d):
    a_term = lambda t: a * ((1 - t) ** 3)
    b_term = lambda t: 3 * b * ((1 - t) ** 2) * t
    c_term = lambda t: 3 * c * (1 - t) * (t ** 2)
    d_term = lambda t: d * (t ** 3)
    return lambda t: a_term(t) + b_term(t) + c_term(t) + d_term(t)

if __name__ == "__main__":
  print Util.get_euclidean_distance(0, 0, 3, 4)
  print Util.is_almost_equal(1, 1.1)
