#!/usr/bin/python
# This is a parser that takes a file of graphics drawing commands and runs
# them. Uses Mr. DW's standards.
# Author: alvin.lin.dev@gmail.com (Alvin Lin)

from lib.color import Color
from lib.drawing import Drawing
from lib.generator import Generator
from lib.matrix import Matrix, TransformationMatrix, EdgeMatrix

import argparse
import sys

class Parser():

    def __init__(self, width=512, height=512, color="#FF0000"):
        """
        Constructor for the Parser class

        Parameters:
        width: int (optional), the width of the image to generate
        height: int (optional), the height of the image to generate
        color: string (optional), the hexadecimal representation of the color to
            use when drawing
        """
        self.width = width
        self.height = height
        self.color = Color(color)
        self.edgematrix = EdgeMatrix()
        self.transformation = TransformationMatrix.identity()

    def parse(self, filename):
        """
        Reads the given file and runs the commands found in the file.

        Parameters:
        filename: str, the name of the file to read from
        """
        with open(filename) as commands_file:
            commands = commands_file.read()
            commands = commands.strip().split("\n")
        i = 0
        try:
            while i < len(commands):
                if commands[i].startswith("#") or len(commands[i]) == 0:
                    i += 1
                elif commands[i] == "dimensions":
                    param_type = "width<number> height<number>"
                    params = map(int, commands[i + 1].split())
                    self.width = params[0]
                    self.height = params[1]
                    i += 2
                elif commands[i] == "line":
                    param_type = "x1<number> y1<number> z1<number>" + \
                    "x2<number> y2<number> z2<number>"
                    params = map(int, commands[i + 1].split())
                    self.edgematrix.add_edge(params[:3], params[3:])
                    i += 2
                elif commands[i] == "circle":
                    param_type = "center_x<number> center_y<number>" + \
                    "radius<number>"
                    params = map(int, commands[i + 1].split())
                    self.edgematrix += Generator.get_circle_edgematrix(
                        params[0], params[1], params[2])
                    i += 2
                elif commands[i] == "hermite":
                    param_type = "x1<number> y1<number> rx1<number> " + \
                    "ry1<number> x2<number> y2<number> rx2<number> ry2<number>"
                    params = map(float, commands[i + 1].split())
                    self.edgematrix += Generator.get_hermite_curve_edgematrix(
                        params[0:2], params[2:4], params[4:6], params[6:8])
                    i += 2
                elif commands[i] == "bezier":
                    param_type = "x1<number> y1<number> ix1<number>" + \
                    "iy1<number> x2<number> y2<number> ix2<number> iy2<number>"
                    params = map(float, commands[i + 1].split())
                    self.edgematrix += Generator.get_bezier_curve_edgematrix(
                        params[0:2], params[2:4], params[4:6], params[6:8])
                    i += 2
                elif commands[i] == "box":
                    param_type = "x<number> y<number> z<number>" + \
                    "width<number height<number> depth<number>"
                    params = map(float, commands[i + 1].split())
                    pointmatrix = Generator.get_box_pointmatrix(
                        params[0], params[1], params[2], params[3], params[4],
                        params[5])
                    self.edgematrix += EdgeMatrix.create_from_pointmatrix(
                        pointmatrix)
                    i += 2
                elif commands[i] == "box_edge":
                    param_type = "x<number> y<number> z<number>" + \
                    "width<number height<number> depth<number>"
                    params = map(float, commands[i + 1].split())
                    self.edgematrix += Generator.get_box_edgematrix(
                        params[0], params[1], params[2], params[3], params[4],
                        params[5])
                    i += 2
                elif commands[i] == "sphere":
                    param_type = "center_x<number> center_y<number>" + \
                    "center_z<number> radius<number>"
                    params = map(float, commands[i + 1].split())
                    pointmatrix = Generator.get_sphere_pointmatrix(
                        params[0], params[1], params[2], params[3])
                    self.edgematrix += EdgeMatrix.create_from_pointmatrix(
                        pointmatrix)
                    i += 2
                elif commands[i] == "torus":
                    param_type = "center_x<number> center_y<number>" + \
                    "center_z<number> radius1<number> radius2<number>"
                    params = map(float, commands[i + 1].split())
                    pointmatrix = Generator.get_torus_pointmatrix(
                        params[0], params[1], params[2], params[3], params[4])
                    self.edgematrix += EdgeMatrix.create_from_pointmatrix(
                        pointmatrix)
                    i += 2
                elif commands[i] == "ident":
                    param_type = "none"
                    self.transformation = TransformationMatrix.identity()
                    i += 1
                elif commands[i] == "scale":
                    param_type = "x<number> y<number> z<number>"
                    params = map(float, commands[i + 1].split())
                    self.transformation.scale(params[0], params[1], params[2])
                    i += 2
                elif commands[i] == "translate":
                    param_type = "x<number> y<number> z<number>"
                    params = map(int, commands[i + 1].split())
                    self.transformation.translate(
                        params[0], params[1], params[2])
                    i += 2
                elif commands[i] == "xrotate":
                    param_type = "theta<number>"
                    params = float(commands[i + 1])
                    self.transformation.rotate_x(params)
                    i += 2
                elif commands[i] == "xrotate_about_point":
                    param_type = "theta<number> x<number> y<number> z<number>"
                    params = map(int, commands[i + 1].split())
                    self.transformation.rotate_x_about_point(
                        params[0], params[1], params[2], params[3])
                    i += 2
                elif commands[i] == "yrotate":
                    param_type = "theta<number>"
                    params = float(commands[i + 1])
                    self.transformation.rotate_y(params)
                    i += 2
                elif commands[i] == "yrotate_about_point":
                    param_type = "theta<number> x<number> y<number> z<number>"
                    params = map(int, commands[i + 1].split())
                    self.transformation.rotate_y_about_point(
                        params[0], params[1], params[2], params[3])
                    i += 2
                elif commands[i] == "zrotate":
                    param_type = "theta<number>"
                    params = float(commands[i + 1])
                    self.transformation.rotate_z(params)
                    i += 2
                elif commands[i] == "zrotate_about_point":
                    param_type = "theta<number> x<number> y<number> z<number>"
                    params = map(int, commands[i + 1].split())
                    self.transformation.rotate_z_about_point(
                        params[0], params[1], params[2], params[3])
                    i += 2
                elif commands[i] == "apply":
                    self.edgematrix *= self.transformation
                    i += 1
                elif commands[i] == "display":
                    drawing = Drawing(self.width, self.height)
                    drawing.draw_edgematrix(self.edgematrix, self.color)
                    drawing.display()
                    i += 1
                elif commands[i] == "save":
                    param_type = "filename<string>"
                    drawing = Drawing(self.width, self.height)
                    drawing.draw_edgematrix(self.edgematrix, self.color)
                    drawing.generate(commands[i + 1])
                    i += 2
                elif commands[i] == "clear":
                    self.edgematrix.clear()
                    i += 1
                elif commands[i] == "quit":
                    break
                else:
                    print "Invalid command at line %d: %s" % (i, commands[i])
                    break
        except (IndexError):
            print "Invalid parameters %s for %s at line %d" % (
                commands[i + 1], commands[i], i)
            print "%s takes the parameters:\n%s" % (commands[i], param_type)
            print sys.exc_info()[0]

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("file", help="The file to generate an image from")
    args = argparser.parse_args()

    parser = Parser()
    parser.parse(args.file)
