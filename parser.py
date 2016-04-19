#!/usr/bin/python
# This is a parser that takes a file of graphics drawing commands and runs
# them. Uses Mr. DW's standards.
# Author: alvin.lin.dev@gmail.com (Alvin Lin)

from lib.color import Color
from lib.drawing import Drawing
from lib.generator import Generator
from lib.matrix import Matrix, TransformationMatrix, EdgeMatrix

import argparse
import traceback

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
        self.drawing = Drawing(self.width, self.height)
        self.color = Color(color)
        self.matrix_stack = TransformationMatrix.identity()

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
                elif commands[i] == "push":
                    param_type = "none"
                    self.drawing.push_matrix()
                    i += 1
                elif commands[i] == "pop":
                    param_type = "none"
                    self.drawing.pop_matrix()
                    i += 1
                elif commands[i] == "ident":
                    param_type = "none"
                    self.drawing.identity()
                    i += 1
                elif commands[i] == "xrotate":
                    param_type = "theta<number>"
                    params = float(commands[i + 1])
                    self.drawing.rotate_x(params)
                    i += 2
                elif commands[i] == "xrotate_about_point":
                    param_type = "theta<number> x<number> y<number> z<number>"
                    params = map(int, commands[i + 1].split())
                    self.drawing.rotate_x_about_point(*params)
                    i += 2
                elif commands[i] == "yrotate":
                    param_type = "theta<number>"
                    params = float(commands[i + 1])
                    self.drawing.rotate_y(params)
                    i += 2
                elif commands[i] == "yrotate_about_point":
                    param_type = "theta<number> x<number> y<number> z<number>"
                    params = map(int, commands[i + 1].split())
                    self.drawing.rotate_y_about_point(*params)
                    i += 2
                elif commands[i] == "zrotate":
                    param_type = "theta<number>"
                    params = float(commands[i + 1])
                    self.drawing.rotate_z(params)
                    i += 2
                elif commands[i] == "zrotate_about_point":
                    param_type = "theta<number> x<number> y<number> z<number>"
                    params = map(int, commands[i + 1].split())
                    self.drawing.rotate_z_about_point(*params)
                    i += 2
                elif commands[i] == "translate":
                    param_type = "x<number> y<number> z<number>"
                    params = map(int, commands[i + 1].split())
                    self.drawing.translate(*params)
                    i += 2
                elif commands[i] == "scale":
                    param_type = "x<number> y<number> z<number>"
                    params = map(float, commands[i + 1].split())
                    self.drawing.scale(*params);
                    i += 2
                elif commands[i] == "line":
                    param_type = "x1<number> y1<number> z1<number> " + \
                    "x2<number> y2<number> z2<number>"
                    params = map(int, commands[i + 1].split())
                    self.drawing.draw_line(*params + [self.color])
                    i += 2
                elif commands[i] == "circle":
                    param_type = "center_x<number> center_y<number> " + \
                    "radius<number>"
                    params = map(int, commands[i + 1].split())
                    self.drawing.draw_circle(*params + [self.color])
                    i += 2
                elif commands[i] == "hermite":
                    param_type = "x1<number> y1<number> rx1<number> " + \
                    "ry1<number> x2<number> y2<number> rx2<number> ry2<number>"
                    params = map(float, commands[i + 1].split())
                    self.draw_hermite_curve(
                        params[0:2], params[2:4], params[4:6], params[6:8],
                        self.color)
                    i += 2
                elif commands[i] == "bezier":
                    param_type = "x1<number> y1<number> ix1<number> " + \
                    "iy1<number> x2<number> y2<number> ix2<number> iy2<number>"
                    params = map(float, commands[i + 1].split())
                    self.draw_bezier_curve(
                        params[0:2], params[2:4], params[4:6], params[6:8],
                        self.color)
                    i += 2
                elif commands[i] == "box":
                    param_type = "x<number> y<number> z<number> " + \
                    "width<number height<number> depth<number>"
                    params = map(float, commands[i + 1].split())
                    self.drawing.draw_box(*params + [self.color])
                    i += 2
                elif commands[i] == "sphere":
                    param_type = "center_x<number> center_y<number> " + \
                    "center_z<number> radius<number>"
                    params = map(float, commands[i + 1].split())
                    self.drawing.draw_sphere(*params + [self.color])
                    i += 2
                elif commands[i] == "torus":
                    param_type = "center_x<number> center_y<number> " + \
                    "center_z<number> radius1<number> radius2<number>"
                    params = map(float, commands[i + 1].split())
                    self.drawing.draw_torus(*params + [self.color])
                    i += 2
                elif commands[i] == "clear":
                    self.drawing.clear();
                    i += 1
                elif commands[i] == "display":
                    self.drawing.display()
                    i += 1
                elif commands[i] == "save":
                    param_type = "filename<string>"
                    self.drawing.generate(commands[i + 1])
                    i += 2
                elif commands[i] == "quit":
                    break
                else:
                    print "Invalid command at line %d: %s" % (i, commands[i])
                    break
        except:
            print "Invalid parameters %s for %s at line %d" % (
                commands[i + 1], commands[i], i)
            print "%s takes the parameters:\n%s" % (commands[i], param_type)
            print traceback.format_exc()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("file", help="The file to generate an image from")
    args = argparser.parse_args()

    parser = Parser()
    parser.parse(args.file)
