#!/usr/bin/python

from lib.color import *
from lib.drawing import *
from lib.matrix import *
from lib.parametric import *

import random

if __name__ == '__main__':
    SIZE = 300;
    d = Drawing(SIZE, SIZE)
    d.draw_edgematrix(a, Color("#ff0000"))
    d.display()
