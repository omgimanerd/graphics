#!/usr/bin/python
# This class encapsulates a vector, which is needed when doing face culling
# in the graphics engine.
# Author: alvin.lin.dev@gmail.com (Alvin Lin)

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
        if not isinstance(vector, list) or len(list) < 3:
            raise TypeError("%s is not a valid Vector representation" % vector)
        else:
            return vector[:3]

    def __str__(self):
        return str(self.vector)

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector([self.vector[0] + other.vector[0],
                           self.vector[1] + other.vector[1],
                           self.vector[2] + other.vector[2]]
        raise TypeError("%s is not a Vector" % other)

    def __iadd__(self, other):
        if isinstance(other, Vector):
            for i in range(3):
                self.vector[i] += other.vector[i]
            return self
        raise TypeError("%s is not a Vector" % other)
