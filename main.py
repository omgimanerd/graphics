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

    drawing.rotate_y(90)

    sphere = Generator.get_sphere_polygonmatrix(0, 250, -250, 200)
    drawing.draw_polygonmatrix(sphere)
    drawing.generate("test")


if __name__ == "__main__":
    main()
