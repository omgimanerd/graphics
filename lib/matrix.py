#!/usr/bin/python
# This class encapsulates matrixes for graphics programming. The Matrix class
# handles the base arithmetic operations associated with matrices while the
# TransformationMatrix class generates transformation matrices to be applied
# to sets of points.
# Author: Alvin Lin

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
    if isinstance(other, Matrix):
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

  def rotateX(self, theta, radians=False):
    if not radians:
      theta = self._d2r(theta)
    self.matrix = (self * TransformationMatrix([[cos(theta), sin(theta), 0, 0],
                                                [-sin(theta), cos(theta), 0, 0],
                                                [0, 0, 1, 0],
                                                [0, 0, 0, 1]]))._matrix()
    return self

  def rotateY(self, theta, radians=False):
    if not radians:
      theta = self._d2r(theta)
    self.matrix = (self * TransformationMatrix([[cos(theta), 0, sin(theta), 0],
                                                [0, 1, 0, 0],
                                                [-sin(theta), 0, cos(theta), 0],
                                                [0, 0, 0, 1]]))._matrix()
    return self

  def rotateZ(self, theta, radians=False):
    if not radians:
      theta = self._d2r(theta)
    self.matrix = (self * TransformationMatrix([[1, 0, 0, 0],
                                                [0, cos(theta), sin(theta), 0],
                                                [0, -sin(theta), cos(theta), 0],
                                                [0, 0, 0, 1]]))._matrix()
    return self

  def translate(self, x, y, z):
    self.matrix = (self * TransformationMatrix([[1, 0, 0, 0],
                                                [0, 1, 0, 0],
                                                [0, 0, 1, 0],
                                                [x, y, z, 1]]))._matrix()
    return self


class EdgeMatrix(Matrix):
  def __init__(self, matrix=None):
    self.counter = 0
    self.matrix = []
    if matrix:
      self.matrix = self._verify(matrix)

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

if __name__ == '__main__':
  m = EdgeMatrix()
  m.add_edge([0, 0], [1, 0, 1])
  print m
