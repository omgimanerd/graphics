#!/usr/bin/python
# This takes an mdl file, compiles it, and runs the commands contained in it.
# Author: alvin.lin.dev@gmail.com (Alvin Lin)

from graphics.lib.color import Color
from graphics.lib.drawing import Drawing
from graphics.lib.matrix import Matrix, TransformationMatrix, EdgeMatrix

import argparse
import mdl
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
        try:
            (commands, symbols) = mdl.parseFile(filename)
        except:
            print "Parsing failed."
            print traceback.format_exc()
        print commands


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("file", help="The file to generate an image from")
    args = argparser.parse_args()

    runner = Runner()
    runner.run(args.file)
