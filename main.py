#!/usr/bin/python

from lib.color import Color
from lib.drawing import Drawing
from lib.matrix import *

import random

if __name__ == '__main__':
  SIZE = 1000;
  ITERATIONS = 1000;
  d = Drawing("test.ppm", SIZE, SIZE)
  square = EdgeMatrix()
  square.add_edge([100, 100], [100, 200])
  square.add_edge([100, 100], [200, 100])
  square.add_edge([100, 200], [200, 200])
  square.add_edge([200, 100], [200, 200])
  square.add_edge([100, 300], [200, 200])

  d.draw_matrix(square, Color("FF0000"))

  a = TransformationMatrix.identity().translate(30, 30, 0).rotateX(10)
  square *= a

  d.draw_matrix(square, Color("FF0000"))
  d.generate()
