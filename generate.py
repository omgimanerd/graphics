#!/usr/bin/python
# Author: Alvin Lin (alvin.lin.dev@gmail.com)

from drawing import Drawing
from color import Color

def main():
  p = Drawing("test.ppm", 500, 500)
  p.draw_bresenham_line(225, 0, 225, 499, Color("FF00FF"))
  p.draw_bresenham_line(275, 499, 275, 0, Color("00FF00"))
  p.draw_bresenham_line(0, 225, 499, 225, Color("FFF000"))
  p.draw_bresenham_line(499, 275, 0, 275, Color("000000"))

  p.draw_bresenham_line(0, 0, 499, 499, Color("0FF0FF"))
  p.draw_bresenham_line(0, 499, 499, 0, Color("0FF0FF"))
  
  p.draw_bresenham_line(0, 0, 499, 400, Color("FF0000")) # 0.8
  p.draw_bresenham_line(0, 0, 400, 499, Color("FF0000")) # 1.2

  p.draw_bresenham_line(499, 0, 0, 400, Color("FF0000")) # -0.8
  p.draw_bresenham_line(499, 0, 100, 499, Color("FF0000")) # -1.2

  p.draw_bresenham_line(499, 499, 0, 100, Color("FF0000")) # 0.8
  p.draw_bresenham_line(499, 499, 100, 0, Color("00FF00")) # 1.2

  p.draw_bresenham_line(0, 499, 400, 0, Color("0000FF")) # -1.2
  p.draw_bresenham_line(0, 499, 499, 100, Color("000FF0")) # -0.8
  p.generate()

if __name__ == "__main__":
  main()
