#!/usr/bin/python

from lib.color import *
from lib.drawing import *
from lib.matrix import *
from lib.parametric import *

import random

if __name__ == '__main__':
    SIZE = 300;
    d = Drawing(SIZE, SIZE)
    d.draw_matrix(EdgeMatrix.get_hermite_curve_matrix([0, 50], [20, 20], [200, 50], [175, 40]), Color("FF0000"))

    d.display()
