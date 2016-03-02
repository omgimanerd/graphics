#!/usr/bin/python
# This class encapsulates matrixes for graphics programming. The Matrix class
# handles the base arithmetic operations associated with matrices while the
# TransformationMatrix class generates transformation matrices to be applied
# to sets of points.
# Author: Alvin Lin

from math import pi, sin, cos

class Matrix():
  def __init__(self, matrix=None):
    self.matrix = []
    if matrix:
      self.matrix = self._verify(matrix)

  def __str__(self):
    return str(self.matrix)

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
        result = [[0] * len(other.matrix[0])] * len(self.matrix)
        for i in range(len(self.matrix)):
          for j in range(len(other.matrix[0])):
            result_row = 0
            for k in range(len(other.matrix)):
              result_row += self.matrix[i][k] * other.matrix[k][j]
            result[i][j] = result_row
        return Matrix(result)
      raise ValueError('Matrices %s and %s cannot be multipled' % (self, other))
    raise TypeError('Cannot add %s to %s' % (other, self))

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

class TransformationMatrix(Matrix):
  def _verify(self, matrix):
    if all([len(x) == 4 for x in matrix]) and len(matrix) == 4:
      return matrix
    raise ValueError('Invalid matrix: %s' % matrix)

  def _r2d(self, theta):
    return (theta / pi) * 180

  @staticmethod
  def identity():
    return TransformationMatrix([[1, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 0, 1]])

  def rotateX(self, theta, radians=False):
    if radians:
      theta = self._r2d(theta)
    self *= TransformationMatrix([[cos(theta), -sin(theta), 0, 0],
                                  [sin(theta), cos(theta), 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1]])
    return self

  def rotateY(self, theta, radians=False):
    if radians:
      theta = self._r2d(theta)
    self *= TransformationMatrix([[cos(theta), 0, -sin(theta), 0],
                                  [0, 1, 0, 0],
                                  [sin(theta), 0, cos(theta), 0],
                                  [0, 0, 0, 1]])
    return self

  def rotateZ(self, theta, radians=False):
    if radians:
      theta = self._r2d(theta)
    self *= TransformationMatrix([[1, 0, 0, 0],
                                  [0, cos(theta), -sin(theta), 0],
                                  [0, sin(theta), cos(theta), 0],
                                  [0, 0, 0, 1]])
    return self

  def translate(self, x, y, z):
    self *= TransformationMatrix([[1, 0, 0, x],
                                  [0, 1, 0, y],
                                  [0, 0, 1, z],
                                  [0, 0, 0, 1]])
    return self

class EdgeMatrix(Matrix):
  def add(self, point):
    pass

if __name__ == '__main__':
  m = Matrix([[0, 0, 0, 1]])
  n = Matrix([[0, 0, 1, 1]])
  print m + n + [0, 1, 0, 1]
