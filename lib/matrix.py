#!/usr/bin/python
# This class encapsulates matrixes for graphics programming. The Matrix class
# handles the base arithmetic operations associated with matrices while the
# TransformationMatrix class generates transformation matrices to be applied
# to sets of points.
# Author: Alvin Lin

from util import Util

from copy import deepcopy
from math import pi, sin, cos

class Matrix():

    def __init__(self, matrix=None):
        """
        Constructor for the Matrix class.

        Parameters:
        matrix, list (optional), a list of lists representing the internal state
            of a Matrix
        """
        self.matrix = []
        if matrix:
            self.matrix = self._verify(matrix)

    def _verify(self, matrix):
        """
        Checks if a given list is a valid representation of a Matrix.

        Parameters:
        matrix: list, the list to check
        """
        if len(matrix) == 0:
            return matrix
        for i in range(len(matrix) - 1):
            if len(matrix[i]) != len(matrix[i + 1]):
                raise ValueError("Invalid matrix: %s" % matrix)
        return matrix

    def _matrix(self):
        """
        Returns the internal representation of this matrix as a list of lists.
        """
        return self.matrix

    def clear(self):
        """
        Clears the matrix.
        """
        self.matrix = []

    def get_rounded(self):
        """
        Returns a copy of this Matrix where every value is rounded to the
        nearest integer and is of type int.
        """
        c = deepcopy(self.matrix)
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                c[i][j] = int(round(self.matrix[i][j]))
        if isinstance(self, TransformationMatrix):
            return TransformationMatrix(c)
        elif isinstance(self, EdgeMatrix):
            return EdgeMatrix(c)
        return Matrix(c)

    def add(self, other):
        """
        Returns an instance of a Matrix containing this Matrix's contents added
        to the other Matrix's contents.

        Parameters:
        other: Matrix, the matrix whose contents will be added to this Matrix
        """
        if type(other) is list:
            other = [other] if len(other) == 4 else [other + [1]]
            return Matrix(self.matrix + other)
        elif isinstance(other, Matrix):
            return Matrix(self.matrix + other.matrix)
        raise ValueError("Cannot add %s to %s" % (self, other))

    def multiply(self, other):
        """
        Returns an instance of a Matrix containing this Matrix's contents
        multiplied by the other Matrix's contents. Will raise an error if the
        two cannot be multiplied.

        Parameters:
        other: Matrix, the matrix whose contents will be multiplied by this
            Matrix
        """
        if isinstance(other, (int, long, float)):
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[i])):
                    self.matrix[i][j] *= other
            return self
        elif isinstance(other, Matrix):
            if len(self.matrix[0]) == len(other.matrix):
                result = [[0 for x in range(
                    len(other.matrix[0]))] for y in range(len(self.matrix))]
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
            raise ValueError(
                "Matrices %s and %s cannot be multipled" % (self, other))
        raise TypeError("Cannot multiply %s and %s" % (other, self))

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
        return self.add(other)

    def __mul__(self, other):
        return self.multiply(other)

    def __iadd__(self, other):
        self = self + other
        return self

    def __imul__(self, other):
        self = self * other
        return self


class TransformationMatrix(Matrix):

    @staticmethod
    def identity():
        """
        Returns an instance of the identity TransformationMatrix.
        """
        return TransformationMatrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])

    def _verify(self, matrix):
        """
        Checks if a given list is a valid representation of a
        TransformationMatrix.

        Parameters:
        matrix: list, the list to check
        """
        if all([len(x) == 4 for x in matrix]) and len(matrix) == 4:
            return matrix
        raise ValueError("Invalid matrix: %s" % matrix)

    def rotate_x(self, theta, radians=False):
        """
        Applies an x rotation to this TransformationMatrix and returns itself
        for method chaining.

        Parameters:
        theta: float or int, the amount in degrees to rotate by, if radians is
            set to True, then this parameter is the amount of radians to rotate
            by
        radians: bool (optional), set this to True if the parameter theta was
            specified in radians
        """
        if not radians:
            theta = Util.d2r(theta)
        self.matrix = (self * TransformationMatrix([
            [cos(theta), sin(theta), 0, 0],
            [-sin(theta), cos(theta), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]]))._matrix()
        return self

    def rotate_y(self, theta, radians=False):
        """
        Applies an y rotation to this TransformationMatrix and returns itself
        for method chaining.

        Parameters:
        theta: float or int, the amount in degrees to rotate by, if radians is
            set to True, then this parameter is the amount of radians to rotate
            by
        radians: bool (optional), set this to True if the parameter theta was
            specified in radians
        """
        if not radians:
            theta = Util.d2r(theta)
        self.matrix = (self * TransformationMatrix([
            [cos(theta), 0, sin(theta), 0],
            [0, 1, 0, 0],
            [-sin(theta), 0, cos(theta), 0],
            [0, 0, 0, 1]]))._matrix()
        return self

    def rotate_z(self, theta, radians=False):
        """
        Applies an z rotation to this TransformationMatrix and returns itself
        for method chaining.

        Parameters:
        theta: float or int, the amount in degrees to rotate by, if radians is
            set to True, then this parameter is the amount of radians to rotate
            by
        radians: bool (optional), set this to True if the parameter theta was
            specified in radians
        """
        if not radians:
            theta = Util.d2r(theta)
        self.matrix = (self * TransformationMatrix([
            [1, 0, 0, 0],
            [0, cos(theta), sin(theta), 0],
            [0, -sin(theta), cos(theta), 0],
            [0, 0, 0, 1]]))._matrix()
        return self

    def translate(self, x, y, z):
        """
        Applies a translation to this TransformationMatrix and returns itself
        for method chaining.

        Parameters:
        x: int, the amount to translate in the x direction
        y: int, the amount to translate in the y direction
        z: int, the amount to translate in the z direction
        """
        self.matrix = (self * TransformationMatrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [x, y, z, 1]]))._matrix()
        return self

    def scale(self, x, y, z):
        """
        Applies a scale transformation to this TransformationMatrix and returns
        itself for method chaining.
        """
        self.matrix = (self * TransformationMatrix([
            [x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1]]))._matrix()
        return self


class EdgeMatrix(Matrix):

    def __init__(self, matrix=None):
        """
        Constructor for the Matrix class.

        Parameters:
        matrix, list (optional), a list of lists representing the internal state
            of an EdgeMatrix
        """
        self.counter = 0
        self.matrix = []
        if matrix:
            self.matrix = self._verify(matrix)

    @staticmethod
    def create_from_pointmatrix(matrix):
        """
        Returns an EdgeMatrix equivalent of a given Matrix of points. Used for
        drawing since each point will be represented as a line of length 1.
        """
        edgematrix = EdgeMatrix()
        for point in matrix:
            edgematrix.add_edge(point, point)
        return edgematrix

    def _verify(self, matrix):
        """
        Checks if a given list is a valid representation of an EdgeMatrix.

        Parameters:
        matrix: list, the list to check
        """
        if len(matrix) % 2 != 0:
            raise ValueError(
                "EdgeMatrix must be initialized with an even number of points")
        if not all([len(x) == 4 for x in matrix]):
            raise ValueError(
                "EdgeMatrix must be initialized with point lists of length 4")
        return matrix

    def _add_point(self, point):
        """
        Adds a point to the EdgeMatrix. This should not be called since it
        will leave the EdgeMatrix in an invalid state if used incorrectly.

        point: list, a list representing a point, can be in the form [x, y] or
            [x, y, z]
        """
        if len(point) > 4 or len(point) == 1:
            raise ValueError("Point %s cannot be added to an EdgeMatrix" %
                             point)
        if len(point) == 2:
            point += [0, 1]
        elif len(point) == 3:
            point += [1]
        self.matrix.append(point)
        return self

    def add_edge(self, p1, p2):
        """
        Adds a line to this EdgeMatrix.

        p1: list, a list representing the first endpoint of the line to add, can
            be in the form [x, y] or [x, y, z]
        p2: list, a list representing the second endpoint of the line to add,
            can be in the form [x, y] or [x, y, z]
        """
        return self._add_point(p1)._add_point(p2)

    def combine(self, edgematrix):
        """
        Concatenates the values of the given EdgeMatrix to the values in this
        EdgeMatrix.


        """
        if not isinstance(edgematrix, EdgeMatrix):
            raise ValueError("%s is not an EdgeMatrix" % edgematrix)
        self.matrix += edgematrix._matrix()

    def __iter__(self):
        return self

    def next(self):
        if self.counter > len(self) - 2:
            self.counter = 0
            raise StopIteration
        edge = self.matrix[self.counter:self.counter + 2]
        self.counter += 2
        return edge

    def __add__(self, other):
        raise NotImplementedError("__add__ cannot be called on an EdgeMatrix")

if __name__ == "__main__":
    m = EdgeMatrix()
    m.add_edge([0, 0], [1, 0, 1])
    print m
