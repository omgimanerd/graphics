#!/usr/bin/python

from lib.color import *
from lib.drawing import *
from lib.matrix import *
from lib.parametric import *

import random

if __name__ == '__main__':
    SIZE = 300;
    d = Drawing(SIZE, SIZE)
    t = TransformationMatrix.identity().rotate_x(34)
    a = EdgeMatrix([
        [0.0, 0.0, 0.0, 0.0],
        [100.0, 100.0, 100.0, 0.0]
        ])
    print a, t
    print a * t
    a *= t

    d.draw_edgematrix(a, Color("#ff0000"))
    d.display()
