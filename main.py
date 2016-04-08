#!/usr/bin/python

from lib.color import Color
from lib.drawing import Drawing
from lib.generator import Generator
from lib.matrix import Matrix, TransformationMatrix, EdgeMatrix
from lib.parametric import Parametric

import random

if __name__ == "__main__":
    SIZE = 400;
    t = TransformationMatrix.identity().rotate_x_about_point(20, 200, 200, 0)
    a = Generator.get_torus_polygonmatrix(200, 200, 0, 150, 200)
    d = Drawing(SIZE, SIZE)
    d.draw_polygonmatrix(a, Color("FF0000"))
    d.display()
