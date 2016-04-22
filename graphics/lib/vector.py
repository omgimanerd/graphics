#!/usr/bin/python
# This class encapsulates a vector, which is needed when doing face culling
# in the graphics engine.
# Author: alvin.lin.dev@gmail.com (Alvin Lin)

from math import acos, sqrt

class Vector():

    def __init__(self, vector=None):
        """
        Constructor for the Vector class. This class is used specifically to
        hold vector for face culling calculations. All vectors will have an
        x, y, and z component represented by the zeroth, first, and second
        index of the internal list.
        """
        self.vector = [0, 0, 0]
        if vector:
            self.vector = Vector._check_vector(vector)

    @staticmethod
    def _check_vector(vector):
        """
        Sanitizes an input into a 3-tuple vector.

        Parameters:
        vector: list, the vector to sanitize.
        """
        if not isinstance(vector, list) or len(vector) < 3:
            raise TypeError("%s is not a valid Vector representation" % vector)
        else:
            return vector[:3]

    @staticmethod
    def dot(v1, v2):
        """
        Returns the dot product of two Vectors.

        Parameters:
        v1: Vector, the first Vector to dot
        v2: Vector, the second Vector to dot
        """
        if isinstance(v1, Vector) and isinstance(v2, Vector):
            return sum([v1[i] * v2[i] for i in range(3)])
        raise TypeError("%s or %s cannot be dotted" % (v1, v2))

    @staticmethod
    def cross(v1, v2):
        """
        Returns the cross product of two Vectors.

        Parameters:
        v1: Vector, the first Vector to cross
        v2: Vector, the second Vector to cross
        """
        if isinstance(v1, Vector) and isinstance(v2, Vector):
            return Vector([
                v1[1] * v2[2] - v1[2] * v2[1],
                v1[2] * v2[0] - v1[0] * v2[2],
                v1[0] * v2[1] - v1[1] * v2[0]
            ])
        raise TypeError("%s or %s cannot be crossed" % (v1, v2))

    @staticmethod
    def get_angle_between(v1, v2):
        """
        Returns the angle between two Vectors.

        Parameters:
        v1: Vector, the first Vector of the angle
        v2: Vector, the second Vector of the angle
        """
        mags = v1.mag() * v2.mag()
        if mags == 0:
            return 0
        return acos(Vector.dot(v1, v2) / mags)

    def __str__(self):
        return str(self.vector)

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector([self.vector[0] + other.vector[0],
                           self.vector[1] + other.vector[1],
                           self.vector[2] + other.vector[2]])
        raise TypeError("%s is not a Vector" % other)

    def __iadd__(self, other):
        if isinstance(other, Vector):
            for i in range(3):
                self[i] += other[i]
            return self
        raise TypeError("%s is not a Vector" % other)

    def __getitem__(self, index):
        return self.vector[index]

    def __setitem__(self, index, value):
        self.vector[index] = value

    def magSquared(self):
        """
        Returns the squared magnitude of this Vector.
        """
        return sum([self[i] * self[i] for i in range(3)])

    def mag(self):
        """
        Returns the magnitude of this Vector.
        """
        return sqrt(self.magSquared())

if __name__ == "__main__":
    a = Vector([3, 4, 0])
    b = Vector([5, 12, 0])
    print a.magSquared()
    print a.mag()
    print Vector.dot(a, b)
