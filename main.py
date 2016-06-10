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
    drawing = Drawing(300, 300)

    drawing.rotate_x_about_point(150, 150, 0, 30)
    drawing.rotate_y_about_point(150, 150, 0, 30)
    drawing.draw_box(150, 150, 0, 10, 40, 20)

    drawing.display()


if __name__ == "__main__":
    main()
