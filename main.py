#!/usr/bin/python

from graphics.lib.color import Color
from graphics.lib.decorators import debug
from graphics.lib.drawing import Drawing
from graphics.lib.generator import Generator
from graphics.lib.matrix import Matrix, TransformationMatrix, EdgeMatrix
from graphics.lib.parametric import Parametric
from graphics.lib.vector import Vector

import random

def main():
    SIZE = 500;
    drawing = Drawing(SIZE, SIZE)

    drawing.push_matrix()
    drawing.translate(250, 250, 0)
    drawing.rotate('x', 45)
    drawing.draw_sphere(0, 0, 0, 200)
    drawing.display()

if __name__ == "__main__":
    main()
