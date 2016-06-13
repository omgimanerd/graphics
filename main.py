#!/usr/bin/python

from graphics.lib.color import Color
from graphics.lib.decorators import debug
from graphics.lib.drawing import Drawing
from graphics.lib.generator import Generator
from graphics.lib.matrix import *
from graphics.lib.parametric import Parametric
from graphics.lib.vector import Vector

import random

def main():
    drawing = Drawing(500, 500)

    drawing.push_matrix()
    drawing.translate(250, 250, 0)
    drawing.set_view_vector(Vector())
    # drawing.rotate_y(45)
    drawing.rotate_x(45)
    drawing.rotate_z(45)
    sphere = Generator.get_torus_polygonmatrix(0, 0, 0, 80, 200)
    drawing.draw_polygonmatrix(sphere)
    # box = Generator.get_box_polygonmatrix(0, 0, 0, 30, 40, 50)
    # drawing.draw_polygonmatrix(box)
    drawing.pop_matrix()

    drawing.display()

if __name__ == "__main__":
    main()
