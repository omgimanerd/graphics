#!/usr/bin/python

from lib.color import Color
from lib.decorators import debug
from lib.drawing import Drawing
from lib.generator import Generator
from lib.matrix import Matrix, TransformationMatrix, EdgeMatrix
from lib.parametric import Parametric
from lib.vector import Vector

import random

def main():
    SIZE = 512;
    c = Color("FF0000")
    drawing = Drawing(SIZE, SIZE)

    args = [0, 0, 0, 300, 0, 0, c]

    drawing.push_matrix()
    drawing.draw_line(*args)
    drawing.translate(75, 50, 0)
    drawing.push_matrix()
    drawing.translate(50, 50, 0)
    drawing.push_matrix()
    drawing.translate(50, 50, 0)
    drawing.draw_line(*args)
    drawing.pop_matrix()
    drawing.draw_line(*args)
    drawing.pop_matrix()
    drawing.draw_line(*args)
    drawing.pop_matrix()

    drawing.push_matrix()
    drawing.rotate_x_about_point(20, 200, 200, 100)
    drawing.rotate_z_about_point(80, 200, 200, 100)
    drawing.draw_torus(200, 200, 100, 20, 80, c, 10, 10)
    drawing.pop_matrix()
    drawing.display()
    drawing.generate("test", "png")

if __name__ == "__main__":
    main()
