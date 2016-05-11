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
    drawing = Drawing(300, 300)

    drawing.push_matrix()
    drawing.translate(150, 150, 0)
    drawing.rotate_x(45)
    drawing.rotate_y(80)
    drawing.rotate_z(70)
    drawing.draw_box(0, 0, 0, 100, 100, 100)
    drawing.pop_matrix()

    drawing.display()


if __name__ == "__main__":
    main()
