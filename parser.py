#!/usr/bin/python
# This is a parser that takes a file of graphics drawing commands and runs
# them.
# Author: alvin.lin.dev@gmail.com (Alvin Lin)

from lib.color import *
from lib.drawing import *
from lib.matrix import *

import argparse

class Parser():
    def __init__(self, width=512, height=512, color='FF0000'):
        self.width = width
        self.height = height
        self.color = Color(color)
        self.edge_matrix = EdgeMatrix()
        self.transformation = None

    def parse(self, filename):
        with open(filename) as args_file:
            args = args_file.read()
            args = args.strip().split("\n")
        i = 0
        while i < len(args):
            if args[i] == 'line':
                params = map(int, args[i + 1].split())
                self.edge_matrix.add_edge(params[:3], params[3:])
                i += 2
            elif args[i] == 'circle':
                params = map(int, args[i + 1].split())
                self.edge_matrix.combine(EdgeMatrix.get_circle_matrix(
                    params[0], params[1], params[2]))
                i += 2
            elif args[i] == 'hermite':
                params = map(float, args[i + 1].split())
                self.edge_matrix.combine(
                    EdgeMatrix.get_hermite_curve_matrix(
                        params[0:2], params[4:6], params[2:4],
                        params[6:8]))
                i += 2
            elif args[i] == 'bezier':
                params = map(float, args[i + 1].split())
                self.edge_matrix.combine(
                    EdgeMatrix.get_bezier_curve_matrix(
                        params[0:2], params[6:8], params[2:4],
                        params[4:6]))
                i += 2
            elif args[i] == 'ident':
                self.transformation = TransformationMatrix.identity()
                i += 1
            elif args[i] == 'scale':
                params = map(float, args[i + 1].split())
                self.transformation.scale(params[0], params[1],
                                          params[2])
                i += 2
            elif args[i] == 'translate':
                params = map(int, args[i + 1].split())
                self.transformation.translate(params[0], params[1],
                                              params[2])
                i += 2
            elif args[i] == 'xrotate':
                params = float(args[i + 1])
                self.transformation.rotate_x(params)
                i += 2
            elif args[i] == 'yrotate':
                params = float(args[i + 1])
                self.transformation.rotate_y(params)
                i += 2
            elif args[i] == 'zrotate':
                params = float(args[i + 1])
                self.transformation.rotate_z(params)
                i += 2
            elif args[i] == 'apply':
                self.edge_matrix *= self.transformation
                i += 1
            elif args[i] == 'display':
                drawing = Drawing(self.width, self.height)
                drawing.draw_matrix(self.edge_matrix, self.color)
                drawing.display()
                i += 1
            elif args[i] == 'save':
                drawing = Drawing(self.width, self.height)
                drawing.draw_matrix(self.edge_matrix, self.color)
                drawing.generate(args[i + 1])
                i += 2
            else:
                raise TypeError('Invalid command %s' % args[i])

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('file', help='The file to generate an image from')
    args = argparser.parse_args()

    parser = Parser()
    parser.parse(args.file)
