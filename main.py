#!/usr/bin/python

from lib.color import Color
from lib.drawing import Drawing
from lib.matrix import Matrix, TransformationMatrix, EdgeMatrix
from lib.parametric import Parametric

import random

if __name__ == "__main__":
    SIZE = 300;
    d = Drawing(SIZE, SIZE)
    d.draw_sphere_points(100, 100, 100, 100, Color("#FF0000"))
    d.display()
    d.generate("test", "png")
