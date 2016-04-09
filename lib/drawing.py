#!/usr/bin/python
# This is a class abstracting the Transformation and Picture classes into a
# general Drawing class.
# ImageMagick must be installed for the generate() and display() methods to
# work.
# Author: Alvin Lin (alvin.lin.dev@gmail.com)

from generator import Generator
from matrix import Matrix, EdgeMatrix, PolygonMatrix
from picture import Picture
from util import Util

from math import pi
from os import system, remove

class Drawing():

    def __init__(self, width, height):
        """
        Constructors for the Drawing class.

        Parameters:
        filename: str, the name of the new image file
        width: int, the width of the image in pixels
        height: int, the height of the image in pixels
        """
        self.width = width
        self.height = height
        self.picture = Picture(width, height)

    def draw_point(self, x, y, color, suppress_error=True):
        """
        Draws a point on the picture.

        Parameters:
        x: int, the x coordinate of the point to draw
        y: int, the y coordinate of the point to draw
        color: Color, the color to draw the point
        suppress_error: bool (optional), when set to True, will suppress
        the error if the point is out of bounds
        """
        self.picture.set_pixel(x, y, color, suppress_error)

    def draw_line(self, x1, y1, x2, y2, color):
        """
        Uses the Bresenham line algorithm to draw a line.

        Parameters:
        x1: int, the x coordinate of one endpoint of the line
        y1: int, the y coordinate of one endpoint of the line
        x2: int, the x coordinate of the other endpoint of the line
        y2: int, the y coordinate of the other endpoint of the line
        color: Color, the color of the line
        """
        dx = x2 - x1
        dy = y2 - y1
        if dx + dy < 0:
            dx *= -1
            dy *= -1
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        if dx == 0:
            while y1 <= y2:
                self.draw_point(x1, y1, color)
                y1 += 1
        elif dy == 0:
            while x1 <= x2:
                self.draw_point(x1, y2, color)
                x1 += 1
        elif dy < 0:
            d = 0
            while x1 <= x2:
                self.draw_point(x1, y1, color)
                if d > 0:
                    y1 += -1
                    d += -dx
                x1 += 1
                d += -dy
        elif dx < 0:
            d = 0
            while y1 <= y2:
                self.draw_point(x1, y1, color)
                if d > 0:
                    x1 += -1
                    d += -dy
                y1 += 1
                d += -dx
        elif dx > dy:
            d = 0
            while x1 <= x2:
                self.draw_point(x1, y1, color)
                if d > 0:
                    y1 += 1
                    d += -dx
                x1 += 1
                d += dy
        else:
            d = 0
            while y1 <= y2:
                self.draw_point(x1, y1, color)
                if d > 0:
                    x1 += 1
                    d += -dy
                y1 += 1
                d += dx

    def draw_pointmatrix(self, matrix, color):
        """
        Draws the given Matrix of points onto the internal raster.

        Parameters:
        matrix: Matrix, the matrix of points to draw
        color: Color, the color to draw the matrix with
        """
        if not isinstance(matrix, Matrix):
            raise TypeError("%s is not a Matrix" % matrix)
        for point in matrix.get_rounded():
            self.draw_point(point[0], point[1], color)

    def draw_edgematrix(self, matrix, color):
        """
        Draws the given EdgeMatrix onto the internal raster as lines.

        Parameters:
        matrix: EdgeMatrix, the matrix of lines to draw
        color: Color, the color to draw the matrix with
        """
        if not isinstance(matrix, EdgeMatrix):
            raise TypeError("%s is not an EdgeMatrix" % matrix)
        for edge in matrix.get_rounded():
            self.draw_line(
                edge[0][0], edge[0][1], edge[1][0], edge[1][1], color)

    def draw_polygonmatrix(self, matrix, color):
        """
        Draws the given PolygonMatrix onto the internal raster.

        Parameters:
        matrix: PolygonMatrix, the matrix of triangles to draw
        color: Color, the color to draw the matrix with
        """
        if not isinstance(matrix, PolygonMatrix):
            raise TypeError("%s is not a PolygonMatrix" % matrix)
        for triangle in matrix.get_rounded():
            self.draw_line(
                triangle[0][0], triangle[0][1], triangle[1][0], triangle[1][1],
                color)
            self.draw_line(
                triangle[1][0], triangle[1][1], triangle[2][0], triangle[2][1],
                color)
            self.draw_line(
                triangle[2][0], triangle[2][1], triangle[0][0], triangle[0][1],
                color)

    def draw_circle(self, center_x, center_y, radius, color, step=50):
        """
        Draws a circle onto the internal raster.

        Parameters:
        center_x: int, the x coordinate of the center of the circle
        center_y: int, the y coordinate of the center of the circle
        radius: int, the radius of the circle
        color: Color, the color of the circle
        step: int (optional), the number of steps to use when drawing splines
        for the circle
        """
        self.draw_edgematrix(Generator.get_circle_edgematrix(
            center_x, center_y, radius, step), color)

    def draw_hermite_curve(self, p1, r1, p2, r2, color, step=100):
        """
        Draws a hermite curve onto the internal raster.

        Parameters:
        p1: list, the first point of the hermite curve
        r1: list, the rate of change at p1
        p2: list, the second point of the hermite curve
        r2: list, the rate of change at p2
        color: Color, the color of the curve
        step: int (optional), the number of steps to use for drawing the curve
        """
        self.draw_edgematrix(Generator.get_hermite_curve_edgematrix(
            p1, r1, p2, r2, step), color)

    def draw_bezier_curve(self, p1, i1, i2, p2, color, step=100):
        """
        Draws a bezier curve onto the internal raster.

        Parameters:
        p1: list, the first endpoint of the bezier curve
        i1: list, the first influence point of the bezier curve
        i2: list, the second influence point of the bezier curve
        p2: list, the second endpoint of the bezier curve
        color: Color, the color of the curve
        step: int (optional), the number of steps to use for drawing the curve
        """
        self.draw_edgematrix(Generator.get_bezier_curve_edgematrix(
            p1, i1, i2, p2, step), color)

    def draw_box_points(self, x, y, z, width, height, depth, color):
        """
        Draws points representing the vertices of a box onto the internal
            raster.

        Parameters:
        x: int, the x coordinate of the front left bottom of the box
        y: int, the y coordinate of the front left bottom of the box
        z: int, the z coordinate of the front left bottom of the box
        width: int, the width of the box
        height: int, the height of the box
        depth: int, the depth of the box
        color: Color, the color of the points
        """
        self.draw_pointmatrix(Generator.get_box_pointmatrix(
            x, y, z, width, height, depth), color)

    def draw_box_edges(self, x, y, z, width, height, depth, color):
        """
        Draws the edges of a box onto the internal raster.

        Parameters:
        x: int, the x coordinate of the front left bottom of the box
        y: int, the y coordinate of the front left bottom of the box
        z: int, the z coordinate of the front left bottom of the box
        width: int, the width of the box
        height: int, the height of the box
        depth: int, the depth of the box
        color: Color, the color of the points
        """
        self.draw_edgematrix(Generator.get_box_edgematrix(
            x, y, z, width, height, depth), color)

    def draw_sphere_points(self, center_x, center_y, center_z, radius, color,
                           theta_step=50, phi_step=50):
        """
        Draws points representing a sphere onto the internal raster.

        Parameters:
        center_x: int, the x coordinate of the center of the sphere
        center_y: int, the y coordinate of the center of the sphere
        center_z: int, the z coordinate of the center of the sphere
        radius: int, the radius of the sphere
        color: Color, the color of the points
        theta_step: int (optional), the number of steps to use when drawing the
            circles
        phi_step: int(optional), the number of steps to use when rotating the
            circles about the center point
        """
        self.draw_pointmatrix(Generator.get_sphere_pointmatrix(
            center_x, center_y, center_z, radius, theta_step, phi_step), color)

    def draw_torus_points(self, center_x, center_y, center_z, radius1, radius2,
                          color, theta_step=100, phi_step=100):
        """
        Generates a Matrix of points representing the points on the surface of
        a torus.

        Parameters:
        center_x: int, the x coordinate of the center of the sphere
        center_y: int, the y coordinate of the center of the sphere
        center_z: int, the z coordinate of the center of the sphere
        radius1: int, the radius of the circle being revolved to make the torus
        radius2: int, the radius of the torus itself
        color: Color, the color of the points
        theta_step: int (optional), the number of steps to use when drawing the
            circle that is revolved to make the torus
        phi_step: int(optional), the number of steps to use when rotating the
            circles about the center point
        """
        self.draw_pointmatrix(Generator.get_torus_pointmatrix(
            center_x, center_y, center_z,
            radius1, radius2, theta_step, phi_step), color)

    def display(self):
        """
        Displays the current state of the internal raster. This method will
        create a temporary ppm file and remove it after displaying.
        """
        filename = hash(self.picture)
        self.generate(filename)
        system("display %s.ppm" % filename)
        remove("%s.ppm" % filename)

    def generate(self, filename, extension="ppm"):
        """
        Turns the internal raster into an image file.

        Parameters:
        filename: str, the name of the image file to generate
        extension: str (optional), the extension of the image file, defaults to
            ppm
        """
        self.picture.generate(filename)
        full_filename = "%s.%s" % (filename, extension)
        if extension != "ppm":
            system("convert %s.ppm %s" % (filename, full_filename))
