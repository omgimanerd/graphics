#!/usr/bin/python

from lib.color import *
from lib.drawing import *
from lib.matrix import *
from lib.parametric import *

import random

if __name__ == '__main__':
  SIZE = 500;
  m = EdgeMatrix.get_hermite_curve_matrix([0, 0], [250, 250],
                                          [100, 0], [200, 200])
  d = Drawing(SIZE, SIZE)
  d.draw_matrix(m, Color("FF0000"))
  # d.draw_circle(25, 50, 10, Color("FF0000"))
  d.display()
