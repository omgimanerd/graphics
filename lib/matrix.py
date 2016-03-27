#!/usr/bin/python
# This class encapsulates matrixes for graphics programming. The Matrix class
# handles the base arithmetic operations associated with matrices while the
# TransformationMatrix class generates transformation matrices to be applied
# to sets of points. The EdgeMatrix class is a bit special and must have an even
# number of elements where every set of two elements represents an edge. when
# iterated through, the elements are returned in sets of two since they are used
# for drawing lines.
# Author: Alvin Lin (alvin.lin.dev@gmail.com)

from util import Util

from copy import deepcopy
from math import pi, sin, cos

class Matrix():

    def __init__(self, matrix=None):
        """
        Constructor for the Matrix class. This class and its subclasses are
        used specifically to hold 4-tuples which represent points. You cannot
        create a Matrix of any other length.

        Parameters:
        matrix, list (optional), a list of lists representing the internal state
            of a Matrix
        """
        self.matrix = []
        if matrix:
            self.matrix = self._check_matrix(matrix)

    @staticmethod
    def _sanitize_point(point):
        """
        Sanitizes an input into a standard 4-tuple point.

        Parameters:
        point: list, the point to sanitize
        """
        if (len(point) > 4 or len(point) < 1) or (
            len(point) == 4 and point[3] != 1) or (
            not all([isinstance(x, (int, float)) for x in point])):
            raise ValueError("%s is not a valid point" % point)
        elif len(point) == 2:
            point += [0, 1]
        elif len(point) == 3:
            point += [1]
        return point

    def _check_matrix(self, matrix):
        """
        Checks if a given list is a valid representation of a Matrix.

        Parameters:
        matrix: list, the list to check
        """
        if len(matrix) == 0 or all([len(x) == 4 for x in matrix]):
            return matrix
        try:
            return map(self._sanitize_point, matrix)
        except ValueError:
            raise ValueError("%s is not a valid matrix representation" % matrix)

    def _matrix(self):
        """
        Returns the internal representation of this matrix as a list of lists.
        """
        return self.matrix

    def add_point(self, point):
        """
        Adds a point to this Matrix's internal representation.

        Parameters:
        point: list, the point to the add to this Matrix
        """
        self.matrix += [Matrix._sanitize_point(point)]
        return self

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
        if isinstance(other, Matrix):
            return Matrix(self.matrix + other.matrix)
        raise ValueError("Cannot add %s to %s" % (self, other))

    def __mul__(self, other):
        if isinstance(other, Matrix) and len(self) > 0 and len(other) > 0:
            if len(self[0]) == len(other.matrix):
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

    def __iadd__(self, other):
        if isinstance(other, Matrix):
            self.matrix += other.matrix
            return self
        raise ValueError("Cannot add %s to %s" % (self, other))

    def __imul__(self, other):
        if isinstance(other, Matrix) and len(self) > 0 and len(other) > 0:
            if len(self.matrix[0]) == len(other.matrix):
                result = [[0 for x in range(
                    len(other.matrix[0]))] for y in range(len(self.matrix))]
                for i in range(len(self.matrix)):
                    for j in range(len(other.matrix[0])):
                        result_row = 0
                        for k in range(len(other.matrix)):
                            result_row += self.matrix[i][k] * other.matrix[k][j]
                        result[i][j] = result_row
                self.matrix = result
                return self
            raise ValueError(
                "Matrices %s and %s cannot be multipled" % (self, other))
        raise TypeError("Cannot multiply %s and %s" % (other, self))


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

    def _check_matrix(self, matrix):
        """
        Checks if a given list is a valid representation of a
        TransformationMatrix.

        Parameters:
        matrix: list, the list to check
        """
        if all([len(x) == 4 for x in matrix]) and len(matrix) == 4:
            return matrix
        raise ValueError("Invalid matrix: %s" % matrix)

    def add_point(self, point):
        raise NotImplementedError(
            "You cannot call add_point on a TransformationMatrix")

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
        self *= TransformationMatrix([
            [cos(theta), sin(theta), 0, 0],
            [-sin(theta), cos(theta), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])
        return self

    def rotate_x_about_point(self, theta, x, y, z, radians=False):
        """
        Applies an x rotation about a point to this TransformationMatrix and
        returns itself for method chaining.

        Parameters:
        theta: float or int, the amount in degrees to rotate by, if radians is
            set to True, then this parameter is the amount of radians to rotate
            by
        x: int, the x coordinate of the point to rotate about
        y: int, the y coordinate of the point to rotate about
        z: int, the z coordinate of the point to rotate about
        radians: bool (optional), set this to True if the parameter theta was
            specified in radians
        """
        self.translate(-x, -y, -z).rotate_x(theta, radians).translate(x, y, z)
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
        self *= TransformationMatrix([
            [cos(theta), 0, sin(theta), 0],
            [0, 1, 0, 0],
            [-sin(theta), 0, cos(theta), 0],
            [0, 0, 0, 1]])
        return self

    def rotate_y_about_point(self, theta, x, y, z, radians=False):
        """
        Applies an y rotation about a point to this TransformationMatrix and
        returns itself for method chaining.

        Parameters:
        theta: float or int, the amount in degrees to rotate by, if radians is
            set to True, then this parameter is the amount of radians to rotate
            by
        x: int, the x coordinate of the point to rotate about
        y: int, the y coordinate of the point to rotate about
        z: int, the z coordinate of the point to rotate about
        radians: bool (optional), set this to True if the parameter theta was
            specified in radians
        """
        self.translate(-x, -y, -z).rotate_y(theta, radians).translate(x, y, z)
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
        self *= TransformationMatrix([
            [1, 0, 0, 0],
            [0, cos(theta), sin(theta), 0],
            [0, -sin(theta), cos(theta), 0],
            [0, 0, 0, 1]])
        return self

    def rotate_z_about_point(self, theta, x, y, z, radians=False):
        """
        Applies an z rotation about a point to this TransformationMatrix and
        returns itself for method chaining.

        Parameters:
        theta: float or int, the amount in degrees to rotate by, if radians is
            set to True, then this parameter is the amount of radians to rotate
            by
        x: int, the x coordinate of the point to rotate about
        y: int, the y coordinate of the point to rotate about
        z: int, the z coordinate of the point to rotate about
        radians: bool (optional), set this to True if the parameter theta was
            specified in radians
        """
        self.translate(-x, -y, -z).rotate_z(theta, radians).translate(x, y, z)
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
        self *= TransformationMatrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [x, y, z, 1]])
        return self

    def scale(self, x, y, z):
        """
        Applies a scale transformation to this TransformationMatrix and returns
        itself for method chaining.
        """
        self *= TransformationMatrix([
            [x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1]])
        return self

    def __add__(self, other):
        raise NotImplementedError(
            "You cannot call __add__ on a TransformationMatrix")


class EdgeMatrix(Matrix):

    def __init__(self, matrix=None):
        """
        Constructor for the Matrix class.

        Parameters:
        matrix, list (optional), a list of lists representing the internal state
            of an EdgeMatrix
        """
        Matrix.__init__(self, matrix)
        self.counter = 0

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

    def _check_matrix(self, matrix):
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

    def add_point(self, point):
        raise NotImplementedError(
            "You cannot call add_point() on an EdgeMatrix")

    def add_edge(self, p1, p2):
        """
        Adds a line/edge to this EdgeMatrix.

        p1: list, a list representing the first endpoint of the line to add, can
            be in the form [x, y] or [x, y, z]
        p2: list, a list representing the second endpoint of the line to add,
            can be in the form [x, y] or [x, y, z]
        """
        self.matrix += [Matrix._sanitize_point(p1)]
        self.matrix += [Matrix._sanitize_point(p2)]
        return self

    def __add__(self, other):
        raise NotImplementedError("You cannot call __add__() on an EdgeMatrix")

    def __iter__(self):
        return self

    def next(self):
        if self.counter > len(self) - 2:
            self.counter = 0
            raise StopIteration
        edge = self.matrix[self.counter:self.counter + 2]
        self.counter += 2
        return edge

if __name__ == "__main__":
    pass
