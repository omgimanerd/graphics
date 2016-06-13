#!/usr/bin/python
# This class encapsulates matrixes for graphics programming. The Matrix class
# handles the base arithmetic operations associated with matrices while the
# TransformationMatrix class generates transformation matrices to be applied
# to sets of points. EdgeMatrix and PolygonMatrix are special subclasses of
# the Matrix class that hold lines and polygons respectively.
# Author: Alvin Lin (alvin.lin.dev@gmail.com)

from util import Util
from vector import Vector

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
            raise TypeError("%s is not a valid point" % point)
        elif len(point) == 2:
            point += [0, 1]
        elif len(point) == 3:
            point += [1]
        return point

    def _preserve_type(self, matrix):
        """
        Casts a list of lists to the type that this Matrix object is.

        Parameters:
        matrix: list, a representation of a Matrix to cast
        """
        if isinstance(self, TransformationMatrix):
            return TransformationMatrix(matrix)
        elif isinstance(self, EdgeMatrix):
            return EdgeMatrix(matrix)
        elif isinstance(self, PolygonMatrix):
            return PolygonMatrix(matrix)
        return Matrix(matrix)

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
        except TypeError:
            raise TypeError("%s is not a valid matrix representation" % matrix)

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

    def copy(self):
        """
        Returns a copy of the matrix.
        """
        return Matrix(self.matrix)

    def get_rounded(self):
        """
        Returns a copy of this Matrix where every value is rounded to the
        nearest integer and is of type int.
        """
        c = deepcopy(self.matrix)
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                c[i][j] = int(round(self.matrix[i][j]))
        return self._preserve_type(c)

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
        raise TypeError("Cannot add %s to %s" % (self, other))

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
                return self._preserve_type(result)
            raise TypeError(
                "Matrices %s and %s cannot be multipled" % (self, other))
        raise TypeError("Cannot multiply %s and %s" % (other, self))

    def __iadd__(self, other):
        if isinstance(other, Matrix):
            self.matrix += other.matrix
            return self
        raise TypeError("Cannot add %s to %s" % (self, other))

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
            raise TypeError(
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
        raise TypeError("Invalid matrix: %s" % matrix)

    def _left_multiply(self, other):
        """
        Returns the result when other is multiplied by this Matrix.

        Parameters:
        matrix: Matrix, the matrix to multiply this matrix into.
        """
        return other * self

    def _ileft_multiply(self, other):
        """
        Sets the result of _left_multiply() back to this object.

        Parameters:
        matrix: Matrix, the matrix to multiply this matrix into.
        """
        self.matrix = self._left_multiply(other).matrix

    def add_point(self, point):
        raise NotImplementedError(
            "You cannot call add_point on a TransformationMatrix")

    def copy(self):
        """
        Returns a copy of the matrix.
        """
        return TransformationMatrix(self.matrix)

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
        self._ileft_multiply(TransformationMatrix([
            [cos(theta), sin(theta), 0, 0],
            [-sin(theta), cos(theta), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]]))
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
        Applies a y rotation to this TransformationMatrix and returns itself
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
        self._ileft_multiply(TransformationMatrix([
            [cos(theta), 0, sin(theta), 0],
            [0, 1, 0, 0],
            [-sin(theta), 0, cos(theta), 0],
            [0, 0, 0, 1]]))
        return self

    def rotate_y_about_point(self, theta, x, y, z, radians=False):
        """
        Applies a y rotation about a point to this TransformationMatrix and
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
        Applies a z rotation to this TransformationMatrix and returns itself
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
        self._ileft_multiply(TransformationMatrix([
            [1, 0, 0, 0],
            [0, cos(theta), sin(theta), 0],
            [0, -sin(theta), cos(theta), 0],
            [0, 0, 0, 1]]))
        return self

    def rotate_z_about_point(self, theta, x, y, z, radians=False):
        """
        Applies a z rotation about a point to this TransformationMatrix and
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
        self._ileft_multiply(TransformationMatrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [x, y, z, 1]]))
        return self

    def scale(self, x, y, z):
        """
        Applies a scale transformation to this TransformationMatrix and returns
        itself for method chaining.

        Parameters:
        x: int or float, the amount to scale in the x direction
        y: int or float, the amount to scale in the y direction
        z: int or float, the amount to scale in the z direction
        """
        self._ileft_multiply(TransformationMatrix([
            [x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1]]))
        return self

    def __add__(self, other):
        raise NotImplementedError(
            "You cannot call __add__ on a TransformationMatrix")


class EdgeMatrix(Matrix):

    def __init__(self, matrix=None):
        """
        Constructor for the EdgeMatrix class.

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
            raise TypeError(
                "EdgeMatrix must be initialized with an even number of points")
        if not all([len(x) == 4 for x in matrix]):
            raise TypeError(
                "EdgeMatrix must be initialized with point lists of length 4")
        return matrix

    def add_point(self, point):
        raise NotImplementedError(
            "You cannot call add_point() on an EdgeMatrix")

    def copy(self):
        """
        Returns a copy of the matrix.
        """
        return EdgeMatrix(self.matrix)

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


class PolygonMatrix(Matrix):

    def __init__(self, matrix=None):
        """
        Constructor for the PolygonMatrix class.

        Parameters:
        matrix, list (optional), a list of lists representing the internal state
            of a PolygonMatrix
        """
        Matrix.__init__(self, matrix)
        self.counter = 0

    def _check_matrix(self, matrix):
        """
        Checks if a given list is a valid representation of a PolygonMatrix.

        Parameters:
        matrix: list, the list to check
        """
        if len(matrix) % 3 != 0:
            raise TypeError(
                "The number of points in a PolygonMatrix must be a multiple" +
                " of 3")
        if not all([len(x) == 4 for x in matrix]):
            raise TypeError(
                "PolygonMatrix must be initialized with lists of length 4")
        return matrix

    def add_point(self, point):
        raise NotImplementedError(
            "You cannot call add_point() on a PolygonMatrix")

    def copy(self):
        """
        Returns a copy of the matrix.
        """
        return PolygonMatrix(self.matrix)

    def add_polygon(self, p1, p2, p3):
        """
        Adds a triangle to this PolygonMatrix.

        p1: list, a list representing the first corner to add, can
            be in the form [x, y] or [x, y, z]
        p2: list, a list representing the second corner to add, can
            be in the form [x, y] or [x, y, z]
        p3: list, a list representing the third corner to add, can
            be in the form [x, y] or [x, y, z]
        """
        self.matrix += [Matrix._sanitize_point(p1)]
        self.matrix += [Matrix._sanitize_point(p2)]
        self.matrix += [Matrix._sanitize_point(p3)]
        return self

    def __add__(self, other):
        raise NotImplementedError(
            "You cannot call __add__() on a PolygonMatrix")

    def __iter__(self):
        return self

    def next(self):
        if self.counter > len(self) - 3:
            self.counter = 0
            raise StopIteration
        edge = self.matrix[self.counter:self.counter + 3]
        self.counter += 3
        return edge

    def cull_faces(self, view_vector):
        """
        Given a Vector representing the view, this method returns a copy of
        this PolygonMatrix minus all the faces that are not visible to the view.

        view_vector: Vector, the view vector to cull in relation to.
        """
        if not isinstance(view_vector, Vector):
            raise TypeError("%s is not valid view Vector" % view_vector)
        culled_polygonmatrix = PolygonMatrix()
        for polygon in self:
            v1 = Vector([
                polygon[2][0] - polygon[0][0],
                polygon[2][1] - polygon[0][1],
                polygon[2][2] - polygon[0][2]
            ])
            v2 = Vector([
                polygon[1][0] - polygon[0][0],
                polygon[1][1] - polygon[0][1],
                polygon[1][2] - polygon[0][2]
            ])
            normal = Vector.cross(v1, v2)
            if Vector.dot(normal, view_vector) < 0:
                culled_polygonmatrix.add_polygon(*polygon)
        return culled_polygonmatrix

if __name__ == "__main__":
    a = Matrix()
