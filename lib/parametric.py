#!/usr/bin/python
# This is a class abstracting a parametric equation.
# Author: alvin.lin.dev@gmail.com (Alvin Lin)

class Parametric():
  def __init__(self, x_function = None, y_function = None, z_function = None):
    self.x_function = x_function;
    self.y_function = y_function;
    self.z_function = z_function;

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
  p = Parametric()
  
