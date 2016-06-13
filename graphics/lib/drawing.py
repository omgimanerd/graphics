#!/usr/bin/python
# This is a class abstracting the Transformation and Picture classes into a
# general Drawing class.
# ImageMagick must be installed for the generate() and display() methods to
# work.
# Author: Alvin Lin (alvin.lin.dev@gmail.com)

from color import Color
from generator import Generator
from matrix import Matrix, TransformationMatrix, EdgeMatrix, PolygonMatrix
from picture import Picture
from util import Util
from vector import Vector

from math import pi
from os import system, remove

class Drawing():

    def __init__(self, width, height):
        """
        Constructors for the Drawing class.

        Parameters:
        width: int, the width of the image in pixels
        height: int, the height of the image in pixels
        """
        self.width = width
        self.height = height
        self.picture = Picture(width, height)
        self.pixel_depths = [[float("-inf") for x in range(
            width)] for y in range(height)]
        self.matrix_stack = [TransformationMatrix.identity()]
        self.view_vector = None

    def _set_pixel(self, x, y, color, suppress_error=True,
                   z_depth=float("-inf")):
        """
        Sets a pixel on the internal raster with reference to the original
        origin (ignoring the current TransformationMatrix).

        Parameters:
        x: int, the x coordinate of the pixel to set
        y: int, the y coordinate of the pixel to set
        color: Color, the color to set the pixel to
        suppress_error: bool (optional), when set to True, will suppress
        the error if the pixel is out of bounds
        z_depth: float (optional), the depth of the pixel, if this pixel is
        lower in depth than the current pixel, then it will not be drawn
        """
        # The coordinates are reversed because of the way lists of lists
        # work in Python.
        try:
            if z_depth >= self.pixel_depths[y][x]:
                self.pixel_depths[y][x] = z_depth
                self.picture.set_pixel(x, y, color)
        except IndexError, exception:
            if not suppress_error:
                raise exception

    def _draw_line(self, x1, y1, x2, y2, color, z_depth=float("-inf")):
        """
        Uses the Bresenham line algorithm to draw a line on the internal
        raster with reference to the original origin (ignoring the current
        TransformationMatrix)

        Parameters:
        x1: int, the x coordinate of one endpoint of the line
        y1: int, the y coordinate of one endpoint of the line
        x2: int, the x coordinate of the other endpoint of the line
        y2: int, the y coordinate of the other endpoint of the line
        color: Color, the color of the line
        z_depth: float (optional), the depth of the line, if this line is lower
        in depth than the pixels that it goes over, then it will not be drawn
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
                self._set_pixel(x1, y1, color, z_depth=z_depth)
                y1 += 1
        elif dy == 0:
            while x1 <= x2:
                self._set_pixel(x1, y1, color, z_depth=z_depth)
                x1 += 1
        elif dy < 0:
            d = 0
            while x1 <= x2:
                self._set_pixel(x1, y1, color, z_depth=z_depth)
                if d > 0:
                    y1 += -1
                    d += -dx
                x1 += 1
                d += -dy
        elif dx < 0:
            d = 0
            while y1 <= y2:
                self._set_pixel(x1, y1, color, z_depth=z_depth)
                if d > 0:
                    x1 += -1
                    d += -dy
                y1 += 1
                d += -dx
        elif dx > dy:
            d = 0
            while x1 <= x2:
                self._set_pixel(x1, y1, color, z_depth=z_depth)
                if d > 0:
                    y1 += 1
                    d += -dx
                x1 += 1
                d += dy
        else:
            d = 0
            while y1 <= y2:
                self._set_pixel(x1, y1, color, z_depth=z_depth)
                if d > 0:
                    x1 += 1
                    d += -dy
                y1 += 1
                d += dx

    def set_view_vector(self, view_vector):
        if not isinstance(view_vector, Vector):
            raise TypeError("%s is not a Vector" % view_vector)
        self.view_vector = view_vector

    def push_matrix(self):
        """
        Pushes a copy of the current TransformationMatrix to the top of the
        stack.
        """
        self.matrix_stack.append(self.get_transformation())

    def pop_matrix(self):
        """
        Pops the current TransformationMatrix from the top of the stack.
        """
        if len(self.matrix_stack) == 1:
            self.matrix_stack = [TranformationMatrix.identity()]
        self.matrix_stack.pop()

    def get_transformation(self):
        """
        Returns the current TransformationMatrix on the stack.
        """
        return self.matrix_stack[-1].copy()

    def apply_transformation(self, matrix):
        """
        Multiplies the current TransformationMatrix on the stack by the given
        TransformationMatrix.

        Parameters:
        matrix: TransformationMatrix, the transformation to apply.
        """
        if not isinstance(matrix, TransformationMatrix):
            raise TypeError("%s is not a TransformationMatrix" % matrix)
        self.matrix_stack[-1] *= matrix

    def identity(self):
        """
        Sets the current TransformationMatrix on the stack to the identity
        matrix.
        """
        self.matrix_stack[-1] = TransformationMatrix.identity()

    def rotate(self, axis, theta, radians=False):
        """
        Applies a rotation to the current TransformationMatrix on the stack.

        Parameters:
        axis: string, the axis to rotate about
        theta: float or int, the amount in degrees to rotate by, if radians is
            set to True, then this parameter is the amount of radians to rotate
            by
        radians: bool (optional), set this to True if the parameter theta was
            specified in radians
        """
        if axis.lower() == "x":
            self.rotate_x(theta, radians=radians)
        elif axis.lower() == "y":
            self.rotate_y(theta, radians=radians)
        elif axis.lower() == "z":
            self.rotate_z(theta, radians=radians)
        else:
            raise ValueError("%s is not a valid axis to rotate about!" % axis)

    def rotate_x(self, theta, radians=False):
        """
        Applies an x rotation to the current TransformationMatrix on the stack.

        Parameters:
        theta: float or int, the amount in degrees to rotate by, if radians is
            set to True, then this parameter is the amount of radians to rotate
            by
        radians: bool (optional), set this to True if the parameter theta was
            specified in radians
        """
        self.matrix_stack[-1].rotate_x(theta, radians=radians)

    def rotate_x_about_point(self, theta, x, y, z, radians=False):
        """
        Applies an x rotation about a point to the current TransformationMatrix
        on the stack.

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
        self.matrix_stack[-1].rotate_x_about_point(theta, x, y, z,
                                                   radians=radians)

    def rotate_y(self, theta, radians=False):
        """
        Applies a y rotation to the current TransformationMatrix on the stack.

        Parameters:
        theta: float or int, the amount in degrees to rotate by, if radians is
            set to True, then this parameter is the amount of radians to rotate
            by
        radians: bool (optional), set this to True if the parameter theta was
            specified in radians
        """
        self.matrix_stack[-1].rotate_y(theta, radians=radians)

    def rotate_y_about_point(self, theta, x, y, z, radians=False):
        """
        Applies an y rotation about a point to the current TransformationMatrix
        on the stack.

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
        self.matrix_stack[-1].rotate_y_about_point(theta, x, y, z,
                                                   radians=radians)

    def rotate_z(self, theta, radians=False):
        """
        Applies a y rotation to the current TransformationMatrix on the stack.

        Parameters:
        theta: float or int, the amount in degrees to rotate by, if radians is
            set to True, then this parameter is the amount of radians to rotate
            by
        radians: bool (optional), set this to True if the parameter theta was
            specified in radians
        """
        self.matrix_stack[-1].rotate_z(theta, radians=radians)

    def rotate_z_about_point(self, theta, x, y, z, radians=False):
        """
        Applies an y rotation about a point to the current TransformationMatrix
        on the stack.

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
        self.matrix_stack[-1].rotate_z_about_point(theta, x, y, z,
                                                   radians=radians)

    def translate(self, x, y, z):
        """
        Applies a translation to the current TransformationMatrix on the stack.

        Parameters:
        x: int, the amount to translate in the x direction
        y: int, the amount to translate in the y direction
        z: int, the amount to translate in the z direction
        """
        self.matrix_stack[-1].translate(x, y, z)

    def scale(self, x, y, z):
        """
        Applies a scale transformation to this TransformationMatrix and returns
        itself for method chaining.

        Parameters:
        x: int or float, the amount to scale in the x direction
        y: int or float, the amount to scale in the y direction
        z: int or float, the amount to scale in the z direction
        """
        self.matrix_stack[-1].scale(x, y, z)

    def draw_pointmatrix(self, matrix, color=Color.BLACK()):
        """
        Draws the given Matrix of points onto the internal raster after
        applying the current TransformationMatrix on the stack.

        Parameters:
        matrix: Matrix, the matrix of points to draw
        color: Color (optional), the color to draw the matrix with
        """
        if not isinstance(matrix, Matrix):
            raise TypeError("%s is not a Matrix" % matrix)
        for point in (matrix * self.get_transformation()).get_rounded():
            self._set_pixel(point[0], point[1], color)

    def draw_edgematrix(self, matrix, color=Color.BLACK()):
        """
        Draws the given EdgeMatrix onto the internal raster as lines after
        applying the current TransformationMatrix on the stack.

        Parameters:
        matrix: EdgeMatrix, the matrix of lines to draw
        color: Color (optional), the color to draw the matrix with
        """
        if not isinstance(matrix, EdgeMatrix):
            raise TypeError("%s is not an EdgeMatrix" % matrix)
        for edge in (matrix * self.get_transformation()).get_rounded():
            self._draw_line(
                edge[0][0], edge[0][1], edge[1][0], edge[1][1], color)

    def draw_polygonmatrix(self, matrix, color=Color.BLACK()):
        """
        Draws the given PolygonMatrix onto the internal raster after applying
        the current TransformationMatrix on the stack.

        Parameters:
        matrix: PolygonMatrix, the matrix of triangles to draw
        cull_view_vector: Vector (optional), the view vector that the faces
          should be culled with, None if the faces should not be culled.
        color: Color (optional), the color to draw the matrix with
        """
        if not isinstance(matrix, PolygonMatrix):
            raise TypeError("%s is not a PolygonMatrix" % matrix)
        matrix *= self.get_transformation()
        if self.view_vector:
            matrix = matrix.cull_faces(self.view_vector)
        for triangle in matrix.get_rounded():
            self._draw_line(
                triangle[0][0], triangle[0][1], triangle[1][0], triangle[1][1],
                color, z_depth=min(triangle[0][2], triangle[1][2]))
            self._draw_line(
                triangle[1][0], triangle[1][1], triangle[2][0], triangle[2][1],
                color, z_depth=min(triangle[1][2], triangle[2][2]))
            self._draw_line(
                triangle[2][0], triangle[2][1], triangle[0][0], triangle[0][1],
                color, z_depth=min(triangle[2][2], triangle[0][2]))

    def fill_polygonmatrix(self, matrix, color=Color.BLACK()):
        """
        Draws and fills the current PolygonMatrix onto the internal raster
        after applying the current TransformationMatrix on the stack.

        Parameters:
        matrix: PolygonMatrix, the matrix of triangles to draw
        cull_view_vector: Vector (optional), the view vector that the faces
          should be culled with, None if the faces should not be culled.
        color: Color (optional), the color to draw the matrix with
        """
        if not isinstance(matrix, PolygonMatrix):
            raise TypeError("%s is not a PolygonMatrix" % matrix)
        matrix *= self.get_transformation()
        if self.view_vector:
            matrix = matrix.cull_faces(self.view_vector)
        for triangle in matrix.get_rounded():
            b = min(triangle, key=lambda point: point[1])
            m = sorted(triangle, key=lambda point: point[1])[1]
            t = max(triangle, key=lambda point: point[1])
            z_depth = min(triangle, key=lambda point: point[2])
            x1, x2 = b[0], b[0]
            dx1 = (t[0] - b[0]) / float(t[1] - b[1]) if t[1] - b[1] else 0
            dx2bm = (m[0] - b[0]) / float(m[1] - b[1]) if m[1] - b[1] else 0
            dx2mt = (t[0] - m[0]) / float(t[1] - m[1]) if t[1] - m[1] else 0
            for y in range(b[1], m[1] + 1):
                self._draw_line(int(x1), y, int(x2), y, color, z_depth=z_depth)
                x1 += dx1
                x2 += dx2bm
            for y in range(m[1], t[1] + 1):
                self._draw_line(int(x1), y, int(x2), y, color, z_depth=z_depth)
                x1 += dx1
                x2 += dx2mt

    def draw_point(self, x, y, z, color=Color.BLACK()):
        """
        Draws the given point onto the internal raster after applying the
        current TransformationMatrix on the stack.

        Parameters:
        x: int, the x coordinate of the point
        y: int, the y coordinate of the point
        z: int, the z coordinate of the point
        color: Color (optional), the color of the line
        """
        self.draw_pointmatrix(Matrix(matrix=[[x, y, z]]), color=color)

    def draw_line(self, x1, y1, z1, x2, y2, z2, color=Color.BLACK()):
        """
        Draws the a line onto the internal raster after applying the current
        TransformationMatrix on the stack.

        Parameters:
        x1: int, the x coordinate of the first endpoint of the line
        y1: int, the y coordinate of the first endpoint of the line
        z1: int, the z coordinate of the first endpoint of the line
        x1: int, the x coordinate of the second endpoint of the line
        y1: int, the y coordinate of the second endpoint of the line
        z1: int, the z coordinate of the second endpoint of the line
        color: Color (optional), the color of the line
        """
        self.draw_edgematrix(EdgeMatrix([[x1, y1, z1, 1], [x2, y2, z2, 1]]),
                             color)

    def draw_circle(self, center_x, center_y, radius,
                    color=Color.BLACK(), step=30):
        """
        Draws a circle onto the internal raster after applying the current
        TransformationMatrix on the stack.

        Parameters:
        center_x: int, the x coordinate of the center of the circle
        center_y: int, the y coordinate of the center of the circle
        radius: int, the radius of the circle
        color: Color (optional), the color of the circle
        step: int (optional), the number of steps to use when drawing splines
        for the circle
        """
        self.draw_edgematrix(Generator.get_circle_edgematrix(
            center_x, center_y, radius, step=step), color)

    def draw_hermite_curve(self, p1, r1, p2, r2,
                           color=Color.BLACK(), step=30):
        """
        Draws a hermite curve onto the internal raster after applying the
        current TransformationMatrix on the stack.

        Parameters:
        p1: list, the first point of the hermite curve
        r1: list, the rate of change at p1
        p2: list, the second point of the hermite curve
        r2: list, the rate of change at p2
        color: Color (optional), the color of the curve
        step: int (optional), the number of steps to use for drawing the curve
        """
        self.draw_edgematrix(Generator.get_hermite_curve_edgematrix(
            p1, r1, p2, r2, step=step), color)

    def draw_bezier_curve(self, p1, i1, i2, p2,
                          color=Color.BLACK(), step=30):
        """
        Draws a bezier curve onto the internal raster after applying the
        current TranformationMatrix on the stack.

        Parameters:
        p1: list, the first endpoint of the bezier curve
        i1: list, the first influence point of the bezier curve
        i2: list, the second influence point of the bezier curve
        p2: list, the second endpoint of the bezier curve
        color: Color (optional), the color of the curve
        step: int (optional), the number of steps to use for drawing the curve
        """
        self.draw_edgematrix(Generator.get_bezier_curve_edgematrix(
            p1, i1, i2, p2, step=step), color)

    def draw_box_points(self, x, y, z, width, height, depth,
                        color=Color.BLACK()):
        """
        Draws points representing the vertices of a box onto the internal
        raster after applying the current TransformationMatrix on the stack.

        Parameters:
        x: int, the x coordinate of the front left bottom of the box
        y: int, the y coordinate of the front left bottom of the box
        z: int, the z coordinate of the front left bottom of the box
        width: int, the width of the box
        height: int, the height of the box
        depth: int, the depth of the box
        color: Color (optional), the color of the points
        """
        self.draw_pointmatrix(Generator.get_box_pointmatrix(
            x, y, z, width, height, depth), color)

    def draw_box(self, x, y, z, width, height, depth,
                 color=Color.BLACK()):
        """
        Draws the polygons of a box onto the internal raster after applying the
        current TransformationMatrix on the stack.

        Parameters:
        x: int, the x coordinate of the front left bottom of the box
        y: int, the y coordinate of the front left bottom of the box
        z: int, the z coordinate of the front left bottom of the box
        width: int, the width of the box
        height: int, the height of the box
        depth: int, the depth of the box
        color: Color (optional), the color of the points
        """
        self.draw_polygonmatrix(Generator.get_box_polygonmatrix(
            x, y, z, width, height, depth), color)

    def draw_sphere_points(self, center_x, center_y, center_z, radius,
                           color=Color.BLACK(), theta_step=30, phi_step=30):
        """
        Draws points representing a sphere onto the internal raster after
        applying the current TransformationMatrix on the stack.

        Parameters:
        center_x: int, the x coordinate of the center of the sphere
        center_y: int, the y coordinate of the center of the sphere
        center_z: int, the z coordinate of the center of the sphere
        radius: int, the radius of the sphere
        color: Color (optional), the color of the points
        theta_step: int (optional), the number of steps to use when drawing the
            circles
        phi_step: int (optional), the number of steps to use when rotating the
            circles about the center point
        """
        self.draw_pointmatrix(Generator.get_sphere_pointmatrix(
            center_x, center_y, center_z, radius,
            theta_step=theta_step, phi_step=phi_step), color)

    def draw_sphere(self, center_x, center_y, center_z, radius,
                    color=Color.BLACK(), theta_step=30, phi_step=30):
        """
        Draws the polygons of a sphere onto the internal raster after
        applying the current TransformationMatrix on the stack.

        Parameters:
        center_x: int, the x coordinate of the center of the sphere
        center_y: int, the y coordinate of the center of the sphere
        center_z: int, the z coordinate of the center of the sphere
        radius: int, the radius of the sphere
        color: Color (optional), the color of the points
        theta_step: int (optional), the number of steps to use when drawing the
        circles
        phi_step: int (optional), the number of steps to use when rotating the
        circles about the center point
        """
        self.draw_polygonmatrix(Generator.get_sphere_polygonmatrix(
            center_x, center_y, center_z, radius,
            theta_step=theta_step, phi_step=phi_step), color)

    def draw_torus_points(self, center_x, center_y, center_z, radius1, radius2,
                          color=Color.BLACK(), theta_step=30, phi_step=30):
        """
        Draws points representing a torus onto the internal raster after
        applying the current TransformationMatrix on the stack.

        Parameters:
        center_x: int, the x coordinate of the center of the sphere
        center_y: int, the y coordinate of the center of the sphere
        center_z: int, the z coordinate of the center of the sphere
        radius1: int, the radius of the circle being revolved to make the torus
        radius2: int, the radius of the torus itself
        color: Color (optional), the color of the points
        theta_step: int (optional), the number of steps to use when drawing the
            circle that is revolved to make the torus
        phi_step: int (optional), the number of steps to use when rotating the
            circles about the center point
        """
        self.draw_pointmatrix(Generator.get_torus_pointmatrix(
            center_x, center_y, center_z, radius1, radius2,
            theta_step=theta_step, phi_step=phi_step), color)

    def draw_torus(self, center_x, center_y, center_z, radius1, radius2,
                   color=Color.BLACK(), theta_step=30, phi_step=30):
        """
        Draws the polygons of a sphere onto the internal raster after
        applying the current TransformationMatrix on the stack.

        Parameters:
        center_x: int, the x coordinate of the center of the sphere
        center_y: int, the y coordinate of the center of the sphere
        center_z: int, the z coordinate of the center of the sphere
        radius1: int, the radius of the circle being revolved to make the torus
        radius2: int, the radius of the torus itself
        color: Color (optional), the color of the points
        theta_step: int (optional), the number of steps to use when drawing the
            circle that is revolved to make the torus
        phi_step: int (optional), the number of steps to use when rotating the
            circles about the center point
        """
        self.draw_polygonmatrix(Generator.get_torus_polygonmatrix(
            center_x, center_y, center_z, radius1, radius2,
            theta_step=theta_step, phi_step=phi_step), color)

    def clear(self):
        """
        Clears the internal raster, setting all pixels back to white.
        """
        self.picture.clear()

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
            remove("%s.ppm" % filename)
