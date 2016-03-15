#!/usr/bin/python

from lib.color import Color
from lib.drawing import Drawing
from lib.matrix import *

import random

if __name__ == '__main__':
  SIZE = 1000;
  ITERATIONS = 1000;
  d = Drawing(SIZE, SIZE)
  square = EdgeMatrix([[0, 0, 0, 1], [0, 50, 0, 1],
                       [0, 0, 0, 1], [50, 0, 0, 1],
                       [0, 50, 0, 1], [50, 50, 0, 1],
                       [50, 0, 0, 1], [50, 50, 0, 1]])
  color = Color('#000000')
  square2 = EdgeMatrix([[899, 899, 0, 1], [899, 999, 0, 1],
                        [899, 899, 0, 1], [999, 899, 0, 1],
                        [899, 999, 0, 1], [999, 999, 0, 1],
                        [999, 899, 0, 1], [999, 999, 0, 1]])
  color2 = Color('#808080')

  rotation = TransformationMatrix().identity().rotate_x(4)

  for i in range(400):
    d.draw_matrix(square, color)
    d.draw_matrix(square2, color2)
    square *= 1.02
    square2 *= 0.95
    color += [20, 10, 5]
    color2 += [5, 10, 20]

  d.generate('test.ppm')
