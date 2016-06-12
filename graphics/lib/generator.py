#!/usr/bin/python
# This class holds static methods for generating matrices of objects.
# Author: alvin.lin.dev@gmail.com (Alvin Lin)
#
from __future__ import division

from decorators import accepts
from parametric import Parametric
from matrix import Matrix, EdgeMatrix, PolygonMatrix
from util import Util

from math import ceil, cos, sin, pi

class Generator():

    @staticmethod
    @accepts((int, float), (int, float), int)
    def get_step_range(min, max, step):
        """
        Generates a list of floats for iterating through when generating
        splines.

        Parameters:
        min: int or float, the minimum to generate from, inclusive
        max: int or float, the maximum to generate to, inclusive
        step: int, the number of steps to break up the interval into
        """
        increment = (max - min) / float(step - 1)
        return [x * increment + min for x in range(step)]

    @staticmethod
    @accepts(int, int, int, int, int)
    def get_knob_range(max_frame, from_frame, to_frame, from_value, to_value):
        knob_range = []
        for i in range(max_frame):
            if i <= from_frame:
                knob_range.append(from_value)
            elif i > to_frame:
                knob_range.append(to_value)
            else:
                knob_range.append(Util.linear_scale(
                    i, from_frame, to_frame, from_value, to_value))
        return knob_range

    @staticmethod
    @accepts((int, float), (int, float), (int, float), (int, float))
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
        def x(t): return cos(t) * radius + center_x
        def y(t): return sin(t) * radius + center_y
        def z(t): return 0
        parametric = Parametric(x, y, z)
        edgematrix = EdgeMatrix()
        step_range = Generator.get_step_range(0, 2 * pi, sides)
        for i in range(len(step_range) - 1):
            edgematrix.add_edge(parametric.get_point(step_range[i]),
                                parametric.get_point(step_range[i + 1]))
        return edgematrix

    @staticmethod
    @accepts((int, float), (int, float), (int, float))
    def get_circle_edgematrix(center_x, center_y, radius, step=30):
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
    @accepts((int, float), (int, float), (int, float), (int, float))
    def get_hermite_function(a, b, c, d):
        """
        Generates a function used for determining the points on a hermite curve.

        Parameters:
        a: int or float, the a coefficient of the equation
        b: int or float, the b coefficient of the equation
        c: int or float, the c coefficient of the equation
        d: int or float, the d coefficient of the equation
        """
        def hermite_function(t): return (a * (t ** 3)) + (b * (t ** 2)) + (
            c * t) + d
        return hermite_function

    @staticmethod
    @accepts(list, list, list, list)
    def get_hermite_curve_edgematrix(p1, r1, p2, r2, step=30):
        """
        Generates an EdgeMatrix of lines representing a hermite curve.

        Parameters:
        p1: list, the first point of the hermite curve
        r1: list, the rate of change at p1
        p2: list, the second point of the hermite curve
        r2: list, the rate of change at p2
        step: int (optional), the number of steps to use when drawing splines
            for the hermite curve
        """
        points = Matrix(matrix=[p1, p2, r1, r2])
        inverse = Matrix([
            [2, -2, 1, 1],
            [-3, 3, -2, -1],
            [0, 0, 1, 0],
            [1, 0, 0, 0]])
        c = inverse * points
        def x(t): return Generator.get_hermite_function(
            c[0][0], c[1][0], c[2][0], c[3][0])(t)
        def y(t): return Generator.get_hermite_function(
            c[0][1], c[1][1], c[2][1], c[3][1])(t)
        def z(t): return 0
        parametric = Parametric(x, y, z)
        edgematrix = EdgeMatrix()
        step_range = Generator.get_step_range(0, 1, step)
        for i in range(len(step_range) - 1):
            edgematrix.add_edge(parametric.get_point(step_range[i]),
                                parametric.get_point(step_range[i + 1]))
        return edgematrix

    @staticmethod
    @accepts((int, float), (int, float), (int, float), (int, float))
    def get_bezier_function(a, b, c, d):
        """
        Generates a function used for determining the points on a bezier curve.

        Parameters:
        a: int or float, the a coefficient of the equation
        b: int or float, the b coefficient of the equation
        c: int or float, the c coefficient of the equation
        d: int or float, the d coefficient of the equation
        """
        def bezier_function(t):
            return (a * ((1 - t) ** 3)) + (3 * b * ((1 - t) ** 2) * t) + (
                3 * c * (1 - t) * (t ** 2)) + (d * (t ** 3))
        return bezier_function

    @staticmethod
    @accepts(list, list, list, list)
    def get_bezier_curve_edgematrix(p1, i1, i2, p2, step=30):
        """
        Generates an EdgeMatrix of lines representing a bezier curve.

        Parameters:
        p1: list, the first endpoint of the bezier curve
        i1: list, the first influence point of the bezier curve
        i2: list, the second influence point of the bezier curve
        p2: list, the second endpoint of the bezier curve
        step: int (optional), the number of steps to use when drawing splines
            for the hermite curve
        """
        def x(t): return Generator.get_bezier_function(
            p1[0], i1[0], i2[0], p2[0])(t)
        def y(t): return Generator.get_bezier_function(
            p1[1], i1[1], i2[1], p2[1])(t)
        def z(t): return 0
        parametric = Parametric(x, y, z)
        edgematrix = EdgeMatrix()
        step_range = Generator.get_step_range(0, 1, step)
        for i in range(len(step_range) - 1):
            edgematrix.add_edge(parametric.get_point(step_range[i]),
                                parametric.get_point(step_range[i + 1]))
        return edgematrix

    @staticmethod
    @accepts((int, float), (int, float), (int, float), (int, float),
             (int, float), (int, float))
    def get_box_pointmatrix(x, y, z, width, height, depth):
        """
        Generates a Matrix of points representing the vertices of a box.
           7-------6
          /|      /|
         / |     / |
        3--|----2  |
        |  4----|--5
        | /     | /
        0-------1

        Parameters:
        x: int, the x coordinate of the front left bottom of the box
        y: int, the y coordinate of the front left bottom of the box
        z: int, the z coordinate of the front left bottom of the box
        width: int, the width of the box
        height: int, the height of the box
        depth: int, the depth of the box
        """
        return Matrix(matrix=[
            [x, y, z, 1],
            [x + width, y, z, 1],
            [x + width, y + height, z, 1],
            [x, y + height, z, 1],
            [x, y, z + depth, 1],
            [x + width, y, z + depth, 1],
            [x + width, y + height, z + depth, 1],
            [x, y + height, z + depth, 1]])

    @staticmethod
    @accepts((int, float), (int, float), (int, float), (int, float),
             (int, float), (int, float))
    def get_box_polygonmatrix(x, y, z, width, height, depth):
        """
        Generates a PolygonMatrix representing the mesh surface of a box.

        Parameters:
        x: int, the x coordinate of the front left bottom of the box
        y: int, the y coordinate of the front left bottom of the box
        z: int, the z coordinate of the front left bottom of the box
        width: int, the width of the box
        height: int, the height of the box
        depth: int, the depth of the box
        """
        pointmatrix = Generator.get_box_pointmatrix(
            x, y, z, width, height, depth)
        return PolygonMatrix(matrix=[
            # Front
            pointmatrix[3], pointmatrix[1], pointmatrix[0],
            pointmatrix[3], pointmatrix[2], pointmatrix[1],
            # Right
            pointmatrix[2], pointmatrix[5], pointmatrix[1],
            pointmatrix[2], pointmatrix[6], pointmatrix[5],
            # Back
            pointmatrix[6], pointmatrix[4], pointmatrix[5],
            pointmatrix[6], pointmatrix[7], pointmatrix[4],
            # Left
            pointmatrix[7], pointmatrix[0], pointmatrix[4],
            pointmatrix[7], pointmatrix[3], pointmatrix[0],
            # Top
            pointmatrix[7], pointmatrix[2], pointmatrix[3],
            pointmatrix[7], pointmatrix[6], pointmatrix[2],
            # Bottom
            pointmatrix[0], pointmatrix[5], pointmatrix[4],
            pointmatrix[0], pointmatrix[1], pointmatrix[5]
        ])

    @staticmethod
    @accepts((int, float), (int, float), (int, float), (int, float))
    def get_sphere_pointmatrix(center_x, center_y, center_z, radius,
                               theta_step=30, phi_step=30):
        """
        Generates a Matrix of points representing the points on the
        surface of a sphere.

        Parameters:
        center_x: int, the x coordinate of the center of the sphere
        center_y: int, the y coordinate of the center of the sphere
        center_z: int, the z coordinate of the center of the sphere
        radius: int, the radius of the sphere
        theta_step: int (optional), the number of steps to use when drawing the
            circles
        phi_step: int(optional), the number of steps to use when rotating the
            circles about the center point
        """
        def x(theta, phi): return radius * cos(theta) + center_x
        def y(theta, phi): return radius * sin(theta) * cos(phi) + center_y
        def z(theta, phi): return radius * sin(theta) * sin(phi) + center_z
        parametric = Parametric(x, y, z)
        matrix = Matrix()
        theta_step_range = Generator.get_step_range(0, 2 * pi, theta_step)
        phi_step_range = Generator.get_step_range(0, pi, phi_step)
        for i in theta_step_range:
            for j in phi_step_range:
                matrix += Matrix([parametric.get_point(i, j)])
        return matrix

    @staticmethod
    @accepts((int, float), (int, float), (int, float), (int, float))
    def get_sphere_polygonmatrix(center_x, center_y, center_z, radius,
                               theta_step=30, phi_step=30):
        """
        Generates a PolygonMatrix representing the mesh surface of a sphere.

        Parameters:
        center_x: int, the x coordinate of the center of the sphere
        center_y: int, the y coordinate of the center of the sphere
        center_z: int, the z coordinate of the center of the sphere
        radius: int, the radius of the sphere
        theta_step: int (optional), the number of steps to use when drawing the
            circles
        phi_step: int(optional), the number of steps to use when rotating the
            circles about the center point
        """
        def x(theta, phi): return radius * cos(theta) + center_x
        def y(theta, phi): return radius * sin(theta) * cos(phi) + center_y
        def z(theta, phi): return radius * sin(theta) * sin(phi) + center_z
        parametric = Parametric(x, y, z)
        matrix = PolygonMatrix()
        points = Generator.get_sphere_pointmatrix(
            center_x, center_y, center_z, radius,
            theta_step=theta_step, phi_step=phi_step)
        for i in range(len(points) - phi_step - 1):
            matrix.add_polygon(points[i],
                               points[i + phi_step + 1],
                               points[i + phi_step])
            matrix.add_polygon(points[i],
                               points[i + 1],
                               points[i + phi_step + 1])
        return matrix

    @staticmethod
    @accepts((int, float), (int, float), (int, float), (int, float),
             (int, float))
    def get_torus_pointmatrix(center_x, center_y, center_z, radius1, radius2,
                              theta_step=30, phi_step=30):
        """
        Generates a Matrix of points representing the points on the surface of
        a torus.

        Parameters:
        center_x: int, the x coordinate of the center of the sphere
        center_y: int, the y coordinate of the center of the sphere
        center_z: int, the z coordinate of the center of the sphere
        radius1: int, the radius of the circle being revolved to make the torus
        radius2: int, the radius of the torus itself
        theta_step: int (optional), the number of steps to use when drawing the
            circle that is revolved to make the torus
        phi_step: int(optional), the number of steps to use when rotating the
            circles about the center point
        """
        def x(theta, phi): return radius1 * cos(theta) + center_x
        def y(theta, phi): return cos(phi) * (
            radius1 * sin(theta) + radius2) + center_y
        def z(theta, phi): return sin(phi) * (
            radius1 * sin(theta) + radius2) + center_z
        parametric = Parametric(x, y, z)
        matrix = Matrix()
        theta_step_range = Generator.get_step_range(0, 2 * pi, theta_step)
        phi_step_range = Generator.get_step_range(0, 2 * pi, phi_step)
        for i in theta_step_range:
            for j in phi_step_range:
                matrix += Matrix([parametric.get_point(i, j)])
        return matrix

    @staticmethod
    @accepts((int, float), (int, float), (int, float), (int, float),
             (int, float))
    def get_torus_polygonmatrix(center_x, center_y, center_z, radius1, radius2,
                                theta_step=30, phi_step=30):
        """
        Generates a PolygonMatrix representing the mesh surface of a torus.

        Parameters:
        center_x: int, the x coordinate of the center of the sphere
        center_y: int, the y coordinate of the center of the sphere
        center_z: int, the z coordinate of the center of the sphere
        radius1: int, the radius of the circle being revolved to make the torus
        radius2: int, the radius of the torus itself
        theta_step: int (optional), the number of steps to use when drawing the
            circle that is revolved to make the torus
        phi_step: int(optional), the number of steps to use when rotating the
            circles about the center point
        """
        matrix = PolygonMatrix()
        points = Generator.get_torus_pointmatrix(
            center_x, center_y, center_z, radius1, radius2,
            theta_step=theta_step, phi_step=phi_step)
        for i in range(len(points) - phi_step - 1):
            matrix.add_polygon(points[i],
                               points[i + phi_step + 1],
                               points[i + phi_step])
            matrix.add_polygon(points[i],
                               points[i + 1],
                               points[i + phi_step + 1])
        return matrix

    @staticmethod
    @accepts((int, float), (int, float), (int, float), (int, float),
             (int, float))
    def get_torus_polygonmatrix_alt(center_x, center_y, center_z, radius1, radius2,
                                theta_step=30, phi_step=30):
        """
        Alternate version of get_torus_polygonmatrix, based off of DW's code. 
        Same for draw, different for fill; More buggy in some ways and less buggy in others.
        Generates a Matrix of points representing the points on the surface of
        a torus.

        Parameters:
        center_x: int, the x coordinate of the center of the sphere
        center_y: int, the y coordinate of the center of the sphere
        center_z: int, the z coordinate of the center of the sphere
        radius1: int, the radius of the circle being revolved to make the torus
        radius2: int, the radius of the torus itself
        theta_step: int (optional), the number of steps to use when drawing the
            circle that is revolved to make the torus
        phi_step: int(optional), the number of steps to use when rotating the
            circles about the center point
        """
        matrix = PolygonMatrix()
        points = Generator.get_torus_pointmatrix(
            center_x, center_y, center_z, radius1, radius2,
            theta_step=theta_step, phi_step=phi_step)
        temp  = []
        for i in range(len(points)):
            temp.append(points[i])
        for i in range(theta_step):
            temp.append(points[i])
        num_points = len(temp)
        num_steps = phi_step
        lat = 0
        lat_stop = num_steps
        longt_stop = num_steps
    
        while lat < lat_stop:
            longt = 0

            while longt < longt_stop:
                #print "lat: " + str(lat)
                #print "longt: " + str(longt)
                index = lat * num_steps + longt

                p0 = temp[ index ]

                p1 = temp[ (index + num_steps) % num_points ]

           
                p2 = temp[ (index + num_steps + 1) % num_points ]

                p3 = temp[ (index + 1) % num_points ]

                matrix.add_polygon(p0, p1, p2)
                matrix.add_polygon(p2, p3, p0)       
            
                longt+= 1
            lat+= 1
        return matrix


if __name__ == "__main__":
    print Generator.get_knob_range(60, 10, 30, 0, 1)
