#!/usr/bin/python

from lib.color import *
from lib.drawing import *
from lib.matrix import *
from lib.parametric import *

import random

if __name__ == '__main__':
    SIZE = 500;
    d = Drawing(SIZE, SIZE)
    c = Color('000000')
    t = TransformationMatrix.identity().translate(-250, -250, 0).rotate_x(
        10).translate(250, 250, 0)

    for i in range(260, 500, 5):
        for j in [2, 4, 10, 25]:
            m = EdgeMatrix.get_circle_matrix(i, i, 30, j)
            for i in range(36):
                d.draw_matrix(m, c)
                m *= t
                c += [random.randint(5, 15), random.randint(5, 15),
                      random.randint(5, 15)]

    d.display()
    d.generate('test.ppm')
