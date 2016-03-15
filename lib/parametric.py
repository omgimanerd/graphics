#!/usr/bin/python
# This is a class abstracting a parametric equation.
# Author: alvin.lin.dev@gmail.com (Alvin Lin)

from math import sin, cos

class Parametric():
  def __init__(self, x_function, y_function, z_function):
    self.x_function = x_function;
    self.y_function = y_function;
    self.z_function = z_function;

  @staticmethod
  def circle_parametric(center_x, center_y, radius):
    x = lambda t: cos(t) * radius + center_x
    y = lambda t: sin(t) * radius + center_y
    z = lambda t: 0
    return Parametric(x_function=x, y_function=y, z_function=z)

  def set_x_function(self, x_function):
    if (not hasattr(x_function, '__call__')):
      raise ValueError('%s is not a function' % x_function)
    self.x_function = x_function

  def set_y_function(self, y_function):
    if (not hasattr(y_function, '__call__')):
      raise ValueError('%s is not a function' % y_function)
    self.y_function = y_function

  def set_z_function(self, z_function):
    if (not hasattr(z_function, '__call__')):
      raise ValueError('%s is not a function' % z_function)
    self.z_function = z_function

  def get_point(self, t):
    return [
      self.x_function(t),
      self.y_function(t),
      self.z_function(t)
    ]

if __name__ == '__main__':
  p = Parametric.circle_parametric()
  print p.get_point(1)
