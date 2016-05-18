#!/usr/bin/python
# Author: Alvin Lin (alvin.lin.dev@gmail.com)
# This is a class that contains utility methods for the Drawing class.

from math import pi

class Util():

    @staticmethod
    def merge_dicts(*args):
        """
        Returns a dictionary of all the merged key value pairs of the
        dictionaries passed in the parameters.

        Parameters:
        args: dict. the dictionaries to merge
        """
        result = {}
        for dictionary in args:
            result.update(dictionary)
        return result

    @staticmethod
    def linear_scale(x, a1, a2, b1, b2):
        """
        Linearly scales a number from one range to another.

        Parameters:
        x: int or float, the number to scale
        a1: int or float, the lower bound of the range to scale from
        a2: int or float, the upper bound of the range to scale from
        b1: int or float, the lower bound of the range to scale to
        b2: int or float, the upper bound of the range to scale to
        """
        return ((x - a1) * (b2 - b1) / (a2 - a1)) + b1

    @staticmethod
    def in_bound(x, lower, upper):
        """
        Returns whether or not a given number is in between two bounds, upper
        bound exclusive. If the specified lower bound is greater than the upper
        bound, they will automatically be switched.

        Parameters:
        x: int or float, the number to check
        lower: int or float, the first bound, usually the lower bound
        upper: int or float, the second bound, usually the upper bound
        """
        if lower > upper:
            lower, upper = upper, lower
        return x >= lower and x < upper

    @staticmethod
    def is_almost_equal(a, b, epsilon=0.1):
        """
        Returns whether or not two numbers are close enough together within a
        threshold epsilon.

        Parameters:
        a: int or float, the first number
        b: int or float, the second number
        epsilon: int or float (optional), the threshold under which the two
            numbers will be considered 'close', defaults to 0.1
        """
        return abs(a - b) <= epsilon

    @staticmethod
    def count_common_values(p1, p2):
        """
        Given two lists of equal length, returns the number of equivalent
        entries. Two list entries are considered equivalent if they have the
        same value and position within the list.

        p1: list, the first list
        p2: list, the second list
        """
        if len(p1) != len(p2):
            raise TypeError("Cannot compare %s and %s" % (p1, p2))
        equals = [p1[i] == p2[i] for i in range(len(p1))]
        return equals.count(True)

    @staticmethod
    def r2d(theta):
        """
        Given an angle theta in radians, returns the equivalent degree measure.

        Parameters:
        theta: int or float, the angle in radians to convert
        """
        return theta / pi * 180.0

    @staticmethod
    def d2r(theta):
        """
        Given an angle theta in degrees, returns the equivalent radian measure.

        Parameters:
        theta: int or float, the angle in degrees to convert
        """
        return theta / 180.0 * pi

if __name__ == "__main__":
    print Util.has_two_points_in_common([1, 1, 2], [1, 0, 2])
