#!/usr/bin/python

from lib.color import Color
from lib.drawing import Drawing
from lib.generator import Generator
from lib.matrix import Matrix, TransformationMatrix, EdgeMatrix
from lib.parametric import Parametric

import random

if __name__ == "__main__":
    SIZE = 300;
    t = TransformationMatrix.identity().rotate_y_about_point(
        30, 100, 100, 0)
    a = EdgeMatrix.create_from_pointmatrix(
        Generator.get_torus_pointmatrix(100, 100, 0, 25, 80))
    d = Drawing(SIZE, SIZE)
    d.draw_edgematrix(a * t, Color("FF0000"))
    d.display()
