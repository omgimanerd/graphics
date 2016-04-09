#!/usr/bin/python
# This is a class abstracting a parametric equation with a variable number of
# inputs that outputs 3-tuple coordinate.
# Author: alvin.lin.dev@gmail.com (Alvin Lin)

from matrix import Matrix

class Parametric():

    def __init__(self, x_function, y_function, z_function):
        """
        Constructor for the Parametric class.

        Parameters:
        x_function: function, the function that determines the x coordinate
        y_function: function, the function that determines the y coordinate
        z_function: function, the function that determines the z coordinate
        """
        self.x_function = x_function;
        self.y_function = y_function;
        self.z_function = z_function;

    def set_x_function(self, x_function):
        """
        Sets the function that determines the x coordinate.

        Parameters:
        x_function, function, the function that determines the x coordinate
        """
        if not hasattr(x_function, "__call__"):
            raise TypeError("%s is not a function" % x_function)
        self.x_function = x_function

    def set_y_function(self, y_function):
        """
        Sets the function that determines the y coordinate.

        Parameters:
        y_function, function, the function that determines the y coordinate
        """
        if (not hasattr(y_function, "__call__")):
            raise TypeError("%s is not a function" % y_function)
        self.y_function = y_function

    def set_z_function(self, z_function):
        """
        Sets the function that determines the z coordinate.

        Parameters:
        z_function, function, the function that determines the z coordinate
        """
        if (not hasattr(z_function, "__call__")):
            raise TypeError("%s is not a function" % z_function)
        self.z_function = z_function

    def get_point(self, *args):
        """
        Calculates and returns a point given some input values.

        Parameters:
        *args, variable number of arguments to input into the x, y, and z
            equations
        """
        return [
            self.x_function(*args),
            self.y_function(*args),
            self.z_function(*args),
            1
        ]

if __name__ == "__main__":
    pass
