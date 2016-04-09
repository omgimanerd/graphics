#!/usr/bin/python

from lib.color import Color
from lib.drawing import Drawing
from lib.generator import Generator
from lib.matrix import Matrix, TransformationMatrix, EdgeMatrix
from lib.parametric import Parametric
from lib.vector import Vector

import random

if __name__ == "__main__":
    SIZE = 400;
    t = TransformationMatrix.identity().rotate_y_about_point(
        45, 200, 200, 0).rotate_z_about_point(0, 200, 200, 0)
    a = Generator.get_torus_polygonmatrix(200, 200, 0, 80, 120)
    b = Generator.get_box_polygonmatrix(200, 200, 0, 50, 80, 120)
    d = Drawing(SIZE, SIZE)
    view = Vector([0, 0, 1])
    d.draw_polygonmatrix((a * t).cull_backfaces(view), Color("FF0000"))
    d.display()
