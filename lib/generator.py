#!/usr/bin/python
# This class holds static methods for generating matrices of objects.
# Author: alvin.lin.dev@gmail.com (Alvin Lin)

from parametric import *
from matrix import *
from util import *

from math import sin, cos, ceil

class Generator():

    @staticmethod
    def get_step_range(min, max, step):
        """
        Generates a list of floats for iterating through when generating
        splines.

        Parameters:
        min: float, the minimum to generate from, inclusive
        max: float, the maximum to generate to, inclusive
        step: float, the number of steps to break up the interval into
        """
        increment = (max - min) / float(step)
        return [x * increment + min for x in range(step + 1)]

    @staticmethod
    def get_polygon_edgematrix(center_x, center_y, radius, sides):
        """
        Generates an EdgeMatrix of lines representing a regular polygon
        centered at the given points inscribed within a circle of the
        given radius.

        Parameters:
        center_x: int, the x coordinate of the center of the polygon
        center_y: int, the y coordinate of the center of the polygon
        radius: int, the radius of the circle
        sides: int, the number of sides in the polygon
        """
        x = lambda t: cos(t) * radius + center_x
        y = lambda t: sin(t) * radius + center_y
        z = lambda t: 0
        parametric = Parametric(x, y, z)
        edgematrix = EdgeMatrix()
        step_range = Generator.get_step_range(0, 2 * pi, sides)
        for i in range(len(step_range) - 1):
            edgematrix.add_edge(parametric.get_point(step_range[i]),
                                parametric.get_point(step_range[i + 1]))
        return edgematrix

    @staticmethod
    def get_circle_edgematrix(center_x, center_y, radius, step=25):
        """
        Generates an EdgeMatrix of lines representing a circle.

        Parameters:
        center_x: int, the x coordinate of the center of the circle
        center_y: int, the y coordinate of the center of the circle
        radius: int, the radius of the circle
        step: int (optional), the number of steps to use when drawing splines
        for the circle
        """
        return Generator.get_polygon_edgematrix(
            center_x, center_y, radius, step)

    @staticmethod
    def get_hermite_curve_edgematrix(p1, r1, p2, r2, step=100):
        """
        Generates an EdgeMatrix of lines representing a hermite curve.

        Parameters:
        p1: list, the first point of the hermite curve
        r1: list, the rate of change at p1
        p2: list, the second point of the hermite curve
        r2: list, the rate of change at p2
        """
        points = Matrix([p1, p2, r1, r2])
        inverse = Matrix([
        [2, -2, 1, 1],
        [-3, 3, -2, -1],
        [0, 0, 1, 0],
        [1, 0, 0, 0]])
        c = inverse * points
        x = lambda t: Util.get_hermite_function(
            c[0][0], c[1][0], c[2][0], c[3][0])(t)
        y = lambda t: Util.get_hermite_function(
            c[0][1], c[1][1], c[2][1], c[3][1])(t)
        z = lambda t: 0
        parametric = Parametric(x, y, z)
        edgematrix = EdgeMatrix()
        step_range = Generator.get_step_range(0, 1, sides)
        for i in range(len(step_range) - 1):
            edgematrix.add_edge(parametric.get_point(step_range[i]),
                                parametric.get_point(step_range[i + 1]))
        return edgematrix

    @staticmethod
    def get_bezier_curve_edgematrix(p1, i1, i2, p2, step=100):
        """
        Generates an EdgeMatrix of lines representing a bezier curve.

        Parameters:
        p1: list, the first endpoint of the bezier curve
        i1: list, the first influence point of the bezier curve
        i2: list, the second influence point of the bezier curve
        p2: list, the second endpoint of the bezier curve
        """
        points = Matrix([p1, i1, i2, p2])
        x = lambda t: Util.get_bezier_function(
            p1[0], i1[0], i2[0], p2[0])(t)
        y = lambda t: Util.get_bezier_function(
            p1[1], i1[1], i2[1], p2[1])(t)
        z = lambda t: 0
        parametric = Parametric(x, y, z)
        edgematrix = EdgeMatrix()
        step_range = Generator.get_step_range(0, 1, sides)
        for i in range(len(step_range) - 1):
            edgematrix.add_edge(parametric.get_point(step_range[i]),
                                parametric.get_point(step_range[i + 1]))
        return edgematrix

    @staticmethod
    def get_box_pointmatrix(center_x, center_y, center_z,
                            width, height, depth):
        pass

    @staticmethod
    def get_sphere_pointmatrix(center_x, center_y, center_z, radius,
                               theta_step=25, phi_step=25):
        """
        Generates a Matrix of points representing the points on the
        surface of a sphere.

        Parameters:
        center_x: int, the x coordinate of the center of the sphere
        center_y: int, the y coordinate of the center of the sphere
        center_z: int, the z coordinate of the center of the sphere
        radius: int, the radius of the sphere
        """
        x = lambda theta, phi: radius * cos(theta) + center_x
        y = lambda theta, phi: radius * sin(theta) * cos(phi) + center_y
        z = lambda theta, phi: radius * sin(theta) * sin(phi) + center_z
        parametric = Parametric(x, y, z)
        matrix = Matrix()
        theta_step_range = Generator.get_step_range(0, 2 * pi, 25)
        phi_step_range = Generator.get_step_range(0, pi, 25)
        for theta in theta_step_range:
            for phi in phi_step_range:
                matrix += parametric.get_point(theta, phi)
        return matrix
