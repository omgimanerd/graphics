#!/usr/bin/python
# Author: Alvin Lin (alvin.lin.dev@gmail.com)

import random

from drawing import Drawing
from color import Color

def main():
  p = Drawing("test.ppm", 400, 400)
  p.stroke_circle(250, 250, 30, Color("#FF00FF"), 3)
  p.draw_line(99, 101, 151, 140, Color("#FF00F0"), 3)
  #p.draw_line(100, 100, 150, 100, Color("FF00FF"), 3)
  #p.stroke_rect(100, 100, 150, 150, Color("FF00FF"), 2)
  p.generate()

if __name__ == "__main__":
  main()
