#!/usr/bin/python
# This class encapsulates matrixes for graphics programming. The Matrix class
# handles the base arithmetic operations associated with matrices while the
# TransformationMatrix class generates transformation matrices to be applied
# to sets of points.
# Author: Alvin Lin

from parametric import *
from util import *

from copy import deepcopy
from math import pi, sin, cos

class Matrix():
  def __init__(self, matrix=None):
    self.matrix = []
    if matrix:
      self.matrix = self._verify(matrix)

  def __str__(self):
    return str(self.matrix)

  def __iter__(self):
    for item in self.matrix:
      yield item

  def __len__(self):
    return len(self.matrix)

  def __getitem__(self, index):
    return self.matrix[index]

  def __neg__(self):
    for i in range(len(self.matrix)):
      for j in range(len(self.matrix[i])):
        self.matrix[i][j] *= -1

  def __add__(self, other):
    if type(other) is list:
      other = [other] if len(other) == 4 else [other + [0]]
      return Matrix(self.matrix + other)
    elif isinstance(other, Matrix):
      return Matrix(self.matrix + other.matrix)
    raise ValueError('Cannot add % to %s' % (self, other))

  def __mul__(self, other):
    if isinstance(other, (int, long, float)):
      for i in range(len(self.matrix)):
        for j in range(len(self.matrix[i])):
          self.matrix[i][j] *= other
      return self
    elif isinstance(other, Matrix):
      if len(self.matrix[0]) == len(other.matrix):
        result = [[0 for x in range(len(other.matrix[0]))] for y in range(
          len(self.matrix))]
        for i in range(len(self.matrix)):
          for j in range(len(other.matrix[0])):
            result_row = 0
            for k in range(len(other.matrix)):
              result_row += self.matrix[i][k] * other.matrix[k][j]
            result[i][j] = result_row
        if isinstance(self, EdgeMatrix):
          return EdgeMatrix(result)
        elif isinstance(self, TransformationMatrix):
          return TransformationMatrix(result)
        return Matrix(result)
      raise ValueError('Matrices %s and %s cannot be multipled' % (self, other))
    raise TypeError('Cannot multiply %s and %s' % (other, self))

  def __iadd__(self, other):
    self = self + other
    return self

  def __imul__(self, other):
    self = self * other
    return self

  def _verify(self, matrix):
    if len(matrix) == 0:
      return matrix
    for i in range(len(matrix) - 1):
      if len(matrix[i]) != len(matrix[i + 1]):
        raise ValueError('Invalid matrix: %s' % matrix)
    return matrix

  def _matrix(self):
    return self.matrix

  def get_rounded(self):
    c = deepcopy(self.matrix)
    for i in range(len(self.matrix)):
      for j in range(len(self.matrix[i])):
        c[i][j] = int(round(self.matrix[i][j]))
    if isinstance(self, TransformationMatrix):
      return TransformationMatrix(c)
    elif isinstance(self, EdgeMatrix):
      return EdgeMatrix(c)
    return Matrix(c)


class TransformationMatrix(Matrix):
  def _verify(self, matrix):
    if all([len(x) == 4 for x in matrix]) and len(matrix) == 4:
      return matrix
    raise ValueError('Invalid matrix: %s' % matrix)

  def _r2d(self, theta):
    return theta / pi * 180.0

  def _d2r(self, theta):
    return theta / 180.0 * pi

  @staticmethod
  def identity():
    return TransformationMatrix([[1, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 0, 1]])

  def rotate_x(self, theta, radians=False):
    if not radians:
      theta = self._d2r(theta)
    self.matrix = (self * TransformationMatrix([
        [cos(theta), sin(theta), 0, 0],
        [-sin(theta), cos(theta), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]]))._matrix()
    return self

  def rotate_y(self, theta, radians=False):
    if not radians:
      theta = self._d2r(theta)
    self.matrix = (self * TransformationMatrix([
        [cos(theta), 0, sin(theta), 0],
        [0, 1, 0, 0],
        [-sin(theta), 0, cos(theta), 0],
        [0, 0, 0, 1]]))._matrix()
    return self

  def rotate_z(self, theta, radians=False):
    if not radians:
      theta = self._d2r(theta)
    self.matrix = (self * TransformationMatrix([
        [1, 0, 0, 0],
        [0, cos(theta), sin(theta), 0],
        [0, -sin(theta), cos(theta), 0],
        [0, 0, 0, 1]]))._matrix()
    return self

  def translate(self, x, y, z):
    self.matrix = (self * TransformationMatrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [x, y, z, 1]]))._matrix()
    return self

  def scale(self, x, y, z):
    self.matrix = (self * TransformationMatrix([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]]))._matrix()
    return self


class EdgeMatrix(Matrix):
  def __init__(self, matrix=None):
    self.counter = 0
    self.matrix = []
    if matrix:
      self.matrix = self._verify(matrix)

  @staticmethod
  def get_polygon_matrix(center_x, center_y, radius, sides):
    """
    Generates an EdgeMatrix of lines representing a regular polygon
    centered at the given points inscribed within a circle of the
    given radius.

    Parameters:
    center_x: int, the x coordinate of the center of the polygon
    center_y: int, the y coordinate of the center of the polygon
    radius: int, the radius of the circle
    sides: int, the number of sides in the polygon
    """
    edge_matrix = EdgeMatrix()
    parametric = Parametric(
        lambda t: cos(t) * radius + center_x,
        lambda t: sin(t) * radius + center_y,
        lambda t: 0)
    counter = 0
    increment = (2 * pi) / sides
    while counter <= 2 * pi:
      edge_matrix.add_edge(parametric.get_point(counter),
                           parametric.get_point(counter + increment))
      counter += increment
    return edge_matrix

  @staticmethod
  def get_circle_matrix(center_x, center_y, radius, step=25):
    """
    Generates an EdgeMatrix of lines representing a circle.

    Parameters:
    center_x: int, the x coordinate of the center of the circle
    center_y: int, the y coordinate of the center of the circle
    radius: int, the radius of the circle
    step: int (optional), the number of steps to use when drawing splines
      for the circle
    """
    return EdgeMatrix.get_polygon_matrix(center_x, center_y, radius, step)

  @staticmethod
  def get_hermite_curve_matrix(p1, r1, p2, r2, step=100):
    """
    Generates an EdgeMatrix of lines representing a hermite curve.

    Parameters:
    p1: list, the first point of the hermite curve
    r1: list, the rate of change at p1
    p2: list, the second point of the hermite curve
    r2: list, the rate of change at p2
    """
    points = Matrix([p1, p2, r1, r2])
    inverse = Matrix([
        [2, -2, 1, 1],
        [-3, 3, -2, -1],
        [0, 0, 1, 0],
        [1, 0, 0, 0]])
    c = inverse * points
    x = lambda t: Util.get_hermite_function(
        c[0][0], c[1][0], c[2][0], c[3][0])(t)
    y = lambda t: Util.get_hermite_function(
        c[0][1], c[1][1], c[2][1], c[3][1])(t)
    z = lambda t: 0
    edge_matrix = EdgeMatrix()
    parametric = Parametric(x, y, z)
    counter = 0
    increment = 1.0 / step
    while counter <= 1:
      edge_matrix.add_edge(parametric.get_point(counter),
                           parametric.get_point(counter + increment))
      counter += increment
    return edge_matrix

  @staticmethod
  def get_bezier_curve_matrix(p1, i1, i2, p2, step=100):
    """
    Generates an EdgeMatrix of lines representing a bezier curve.

    Parameters:
    p1: list, the first endpoint of the bezier curve
    i1: list, the first influence point of the bezier curve
    i2: list, the second influence point of the bezier curve
    p2: list, the second endpoint of the bezier curve
    """
    points = Matrix([p1, i1, i2, p2])
    x = lambda t: Util.get_bezier_function(
        p1[0], i1[0], i2[0], p2[0])(t)
    y = lambda t: Util.get_bezier_function(
        p1[1], i1[1], i2[1], p2[1])(t)
    z = lambda t: 0
    edge_matrix = EdgeMatrix()
    parametric = Parametric(x, y, z)
    counter = 0
    increment = 1.0 / step
    while counter <= 1:
      edge_matrix.add_edge(parametric.get_point(counter),
                           parametric.get_point(counter + increment))
      counter += increment
    return edge_matrix

  def __iter__(self):
    return self

  def next(self):
    if self.counter > len(self) - 2:
      self.counter = 0
      raise StopIteration
    edge = self.matrix[self.counter:self.counter + 2]
    self.counter += 2
    return edge

  def _verify(self, matrix):
    if len(matrix) % 2 != 0:
      raise ValueError(
        'EdgeMatrix must be initialized with an even number of points')
    if not all([len(x) == 4 for x in matrix]):
      raise ValueError(
        'EdgeMatrix must be initialized with point lists of length 4')
    return matrix

  def __add__(self, other):
    raise NotImplementedError('__add__ cannot be called on an EdgeMatrix')

  def _add_point(self, point):
    if len(point) == 2:
      point += [0, 1]
    elif len(point) == 3:
      point += [1]
    self.matrix.append(point)

  def add_edge(self, point1, point2):
    self._add_point(point1)
    self._add_point(point2)
    return self

  def combine(self, edge_matrix):
    self.matrix += edge_matrix._matrix()

if __name__ == '__main__':
  m = EdgeMatrix()
  m.add_edge([0, 0], [1, 0, 1])
  print m
