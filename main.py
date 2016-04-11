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
    SIZE = 400;
    t = TransformationMatrix.identity().rotate_y_about_point(
        45, 200, 200, 0).rotate_z_about_point(0, 200, 200, 0).translate(
        -20, 30, 0)
    drawing = Drawing(SIZE, SIZE)
    view = Vector([0, 0, 1])

    a = Generator.get_torus_polygonmatrix(350, 50, 0, 20, 40, 20, 20)
    b = Generator.get_torus_polygonmatrix(250, 100, 0, 15, 30, 20, 20)
    c = Generator.get_torus_polygonmatrix(175, 140, 0, 10, 20, 20, 20)
    d = Generator.get_torus_polygonmatrix(175, 200, 0, 10, 20, 20, 20)
    e = Generator.get_torus_polygonmatrix(250, 240, 0, 15, 30, 20, 20)
    f = Generator.get_torus_polygonmatrix(350, 290, 0, 20, 40, 20, 20)

    drawing.draw_polygonmatrix((a * t).cull_backfaces(view), Color("FF0000"))
    drawing.draw_polygonmatrix((b * t).cull_backfaces(view), Color("00FF00"))
    drawing.draw_polygonmatrix((c * t).cull_backfaces(view), Color("0000FF"))
    drawing.draw_polygonmatrix((d * t).cull_backfaces(view), Color("FF0000"))
    drawing.draw_polygonmatrix((e * t).cull_backfaces(view), Color("00FF00"))
    drawing.draw_polygonmatrix((f * t).cull_backfaces(view), Color("0000FF"))
    drawing.display()
    drawing.generate("test", "png")

if __name__ == "__main__":
    main()
