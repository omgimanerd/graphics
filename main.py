#!/usr/bin/python

from lib.color import Color
from lib.drawing import Drawing
from lib.matrix import *

import random

if __name__ == '__main__':
  SIZE = 100;
  d = Drawing(SIZE, SIZE)
  d.draw_circle(50, 50, 30, Color("FF0000"))

  d.generate('test.ppm')
