#!/usr/bin/python

from lib.color import Color
from lib.drawing import Drawing

import random

if __name__ == '__main__':
  SIZE = 100;
  ITERATIONS = 1000;
  d = Drawing("test.ppm", SIZE, SIZE)
  for i in range(ITERATIONS):
    x1 = random.randint(0, SIZE - 1);
    y1 = random.randint(0, SIZE - 1);
    x2 = random.randint(0, SIZE - 1);
    y2 = random.randint(0, SIZE - 1);
    d.draw_bresenham_line(x1, y1, x2, y2, Color.random())
  d.generate()
