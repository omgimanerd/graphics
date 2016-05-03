#!/usr/bin/python
# This takes an mdl file, compiles it, and runs the commands contained in it.
# Author: alvin.lin.dev@gmail.com (Alvin Lin)

import graphics.compiler.mdl as mdl

from graphics.lib.color import Color
from graphics.lib.drawing import Drawing
from graphics.lib.matrix import Matrix, TransformationMatrix, EdgeMatrix

import argparse
import traceback

class Runner():

    def __init__(self, width=512, height=512, color="#FF0000"):
        """
        Constructor for the Runner class.

        Parameters:
        width: int (optional), the width of the image to generate
        height: int (optional), the height of the image to generate
        color: string (optional), the hexadecimal representation of the color to
            use when drawing
        """
        self.width = width
        self.height = height
        self.drawing = Drawing(width, height)
        self.color = Color(color)

    def run(self, filename):
        """
        Reads the given file, compiles the code found in it, and runs it.

        Parameters:
        filename: str, the name of the file to read from
        """
        command_translate = {
            'push': self.drawing.push_matrix,
            'pop': self.drawing.pop_matrix,
            'identity': self.drawing.identity,
            'rotate': self.drawing.rotate,
            'translate': self.drawing.translate,
            'move': self.drawing.translate,
            'scale': self.drawing.scale,
            'line': self.drawing.draw_line,
            'circle': self.drawing.draw_circle,
            'hermite': self.drawing.draw_hermite_curve,
            'bezier': self.drawing.draw_bezier_curve,
            'box': self.drawing.draw_box,
            'sphere': self.drawing.draw_sphere,
            'torus': self.drawing.draw_torus,
            'display': self.drawing.display,
            'generate': self.drawing.generate
        }
        commands = None
        symbols = None
        try:
            (commands, symbols) = mdl.parseFile(filename)
        except:
            print "Parsing failed."
            print traceback.format_exc()
            return

        try:
            for command in commands:
                name = command[0]
                args = filter(lambda x: x is not None, command[1:])
                command_translate[name](*args)
        except:
            print "Execution failed."
            print traceback.format_exc()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("file", help="The mdl file to run")
    args = argparser.parse_args()

    runner = Runner()
    runner.run(args.file)
