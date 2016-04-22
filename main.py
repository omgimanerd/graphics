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
    drawing.translate(400, 400, 0)

    for i in range(10):
        drawing.rotate_x_about_point(36, 250, 250, 0)
        drawing.push_matrix()
        drawing.rotate_z(10)
        drawing.draw_torus(0, 0, 0, 20, 40, Color.random(), theta_step=20,
                           phi_step=20)
        drawing.pop_matrix()

    drawing.pop_matrix()

    drawing.push_matrix()
    drawing.translate(400, 100, 0)
    for i in range(10):
        drawing.rotate_x_about_point(36, 250, 250, 0)
        drawing.push_matrix()
        drawing.rotate_y(10)
        drawing.draw_torus(0, 0, 0, 20, 40, Color.random(), theta_step=20,
                           phi_step=20)
        drawing.pop_matrix()

    drawing.pop_matrix()
    drawing.draw_sphere(250, 250, 0, 50, Color.random())


    drawing.display()
    drawing.generate("test", "png")

if __name__ == "__main__":
    main()
