#!/usr/bin/python
# Author: Alvin Lin (alvin.lin.dev@gmail.com)

import random

from drawing import Drawing
from color import Color

def main():
  p = Drawing("test.ppm", 500, 500)
  p.stroke_circle(100, 250, 30, Color("#FF00FF"), 3)
  p.fill_circle(100, 100, 50, Color("00F0FF"))
  p.fill_circle(250, 50, 50, Color("FF0000"))
  # p.draw_line(0, 100, 200, 400, Color("#FF00F0"), 4)
  p.draw_line(100, 100, 150, 100, Color("FF00FF"), 3)
  #p.stroke_rect(100, 100, 150, 150, Color("FF00FF"), 2)
  p.generate()

if __name__ == "__main__":
  main()
