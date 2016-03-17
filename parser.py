#!/usr/bin/python
# This is a parser that takes a file of graphics drawing commands and runs
# them.
# Author: alvin.lin.dev@gmail.com (Alvin Lin)

from lib.color import *
from lib.drawing import *
from lib.matrix import *

import argparse

class Parser():
  def __init__(self, width=512, height=512):
    self.drawing = Drawing(width, height)
    self.transformation = None

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
