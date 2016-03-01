#!/usr/bin/python
# This class encapsulates matrixes for graphics programming.
# Author: Alvin Lin

from math import pi

class Matrix():
  def __init__(self, matrix=[]):
    self.matrix = self._verify(matrix)

  def __str__(self):
    return str(self.matrix)

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
        result = [[x for x in range(len(other.matrix[0]))] for y in range(
          len(self.matrix))]
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
    if all(map(lambda x: len(x) == 4, matrix)) and len(matrix) == 4:
      return matrix
    raise ValueError('Invalid matrix: %s' % matrix)
  
  def _r2d(self, theta):
    # Floating point number may cause inefficiency?
    # WONTFIX
    return (theta / pi) * 180

  @staticmethod
  def identity():
    return TransformationMatrix([[1, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 0, 1]])

  def compose_rotationX(theta, radians=False):
    if radians:
      theta = self._r2d(theta)
    pass

  def compose_rotationY(theta, radians=False):
    if radians:
      theta = self._r2d(theta)
    pass

  def compose_rotationZ(theta, radians=False):
    if radians:
      theta = self._r2d(theta)
    pass

  def compose_translation(x, y, z):
    self *= [[1, 0, 0, x],
             [0, 1, 0, y],
             [0, 0, 1, z],
             [0, 0, 0, 1]]

if __name__ == '__main__':
  pass
