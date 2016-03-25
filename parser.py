#!/usr/bin/python
# This is a parser that takes a file of graphics drawing commands and runs
# them.
# Author: alvin.lin.dev@gmail.com (Alvin Lin)

from lib.color import Color
from lib.drawing import Drawing
from lib.generator import Generator
from lib.matrix import Matrix, TransformationMatrix, EdgeMatrix

import argparse

class Parser():

    def __init__(self, width=512, height=512, color='FF0000'):
        self.width = width
        self.height = height
        self.color = Color(color)
        self.edgematrix = EdgeMatrix()
        self.transformation = TransformationMatrix.identity()

    def parse(self, filename):
        with open(filename) as args_file:
            args = args_file.read()
            args = args.strip().split("\n")
        i = 0
        while i < len(args):
            if args[i][0] == '#' or len(args[i]) == 0:
                i += 1
            elif args[i] == 'line':
                params = map(int, args[i + 1].split())
                self.edgematrix.add_edge(params[:3], params[3:])
                i += 2
            elif args[i] == 'circle':
                params = map(int, args[i + 1].split())
                self.edgematrix.combine(Generator.get_circle_edgematrix(
                    params[0], params[1], params[2]))
                i += 2
            elif args[i] == 'hermite':
                params = map(float, args[i + 1].split())
                self.edgematrix.combine(
                    Generator.get_hermite_curve_edgematrix(
                        params[0:2], params[2:4],
                        params[4:6], params[6:8]))
                i += 2
            elif args[i] == 'bezier':
                params = map(float, args[i + 1].split())
                self.edgematrix.combine(
                    Generator.get_bezier_curve_edgematrix(
                        params[0:2], params[2:4],
                        params[4:6], params[6:8]))
                i += 2
            elif args[i] == 'box':
                params = map(float, args[i + 1].split())
                pointmatrix = Generator.get_box_pointmatrix(
                    params[0], params[1], params[2], params[3], params[4],
                    params[5])
                self.edgematrix.combine(EdgeMatrix.create_from_pointmatrix(
                    pointmatrix))
                i += 2
            elif args[i] == 'sphere':
                params = map(float, args[i + 1].split())
                pointmatrix = Generator.get_sphere_pointmatrix(
                    params[0], params[1], params[2], params[3])
                self.edgematrix.combine(EdgeMatrix.create_from_pointmatrix(
                    pointmatrix))
                i += 2
            elif args[i] == 'torus':
                params = map(float, args[i + 1].split())
                pointmatrix = Generator.get_torus_pointmatrix(
                    params[0], params[1], params[2], params[3], params[4])
                self.edgematrix.combine(EdgeMatrix.create_from_pointmatrix(
                    pointmatrix))
                i += 2
            elif args[i] == 'ident':
                self.transformation = TransformationMatrix.identity()
                i += 1
            elif args[i] == 'scale':
                params = map(float, args[i + 1].split())
                self.transformation.scale(params[0], params[1], params[2])
                i += 2
            elif args[i] == 'translate':
                params = map(int, args[i + 1].split())
                self.transformation.translate(params[0], params[1], params[2])
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
                self.edgematrix *= self.transformation
                i += 1
            elif args[i] == 'display':
                drawing = Drawing(self.width, self.height)
                drawing.draw_edgematrix(self.edgematrix, self.color)
                drawing.display()
                i += 1
            elif args[i] == 'save':
                drawing = Drawing(self.width, self.height)
                drawing.draw_matrix(self.edgematrix, self.color)
                drawing.generate(args[i + 1])
                i += 2
            elif args[i] == 'clear':
                self.edgematrix.clear()
            elif args[i] == 'quit':
                break
            else:
                raise TypeError('Invalid command %s' % args[i])

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('file', help='The file to generate an image from')
    args = argparser.parse_args()

    parser = Parser()
    parser.parse(args.file)
