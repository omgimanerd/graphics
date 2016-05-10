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

    print map(str, drawing.matrix_stack)

    drawing.push_matrix()
    drawing.translate(150, 150, 0)
    drawing.draw_line(0, 0, 0, 100, 100, 0, Color.GREEN())
    drawing.pop_matrix()

    drawing.push_matrix()
    drawing.translate(150, 150, 0)
    drawing.rotate_x(30);
    print drawing.get_transformation()
    drawing.draw_line(0, 0, 0, 100, 100, 0, Color.RED())
    drawing.pop_matrix()

    drawing.display()


if __name__ == "__main__":
    main()
