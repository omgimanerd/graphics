#!/usr/bin/python
# Author: Alvin Lin (alvin.lin.dev@gmail.com)
# This is a class that manages colors for the Picture and Drawing class.

import random

class Color:

    def __init__(self, color):
        """
        Constructor for the Color class.

        Parameters:
        color: str or list, the hexadecimal or rgb representation of the color
        """
        if type(color) is list and len(color) == 3:
            self.color = color
        elif type(color) is str:
            self.color = self._hex_to_rgb(color)
        else:
            raise TypeError(
                "Invalid color, only hex or a list of RGB values are allowed.")

    @staticmethod
    def random():
        """
        Returns a randomly generated color.
        """
        return Color([random.randint(0, 256) for x in range(3)])

    @staticmethod
    def _hex_to_rgb(hex_code):
        """
        Given the hexdecimal representation of a color, this returns the rgb
        representation of the given color.

        Parameters:
        hex_code: str, the hex code to convert to rgb

        http://stackoverflow.com/questions/214359/
        converting-hex-color-to-rgb-and-vice-versa
        """
        hex_code = hex_code.lstrip("#")
        lv = len(hex_code)
        return [
            int(hex_code[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)]

    @staticmethod
    def BLACK():
        return Color("000000")

    @staticmethod
    def WHITE():
        return Color("FFFFFF")

    @staticmethod
    def RED():
        return Color("FF0000")

    @staticmethod
    def GREEN():
        return Color("00FF00")

    @staticmethod
    def BLUE():
        return Color("0000FF")

    def __iter__(self):
        for c in self.color:
            yield c

    def __str__(self):
        return str(self.color)

    def __len__(self):
        return len(self.color)

    def __add__(self, other):
        if isinstance(other, (list, Color)) and len(other) == 3:
            return Color([
                int(self[0] + other[0]) % 256,
                int(self[1] + other[1]) % 256,
                int(self[2] + other[2]) % 256])
        raise TypeError("Cannot add %s to %s:" % (self, other))

    def __iadd__(self, other):
        self = self + other
        return self

    def __getitem__(self, index):
        if index >= 0 and index <= 2:
            return self.color[index]
        raise IndexError("Index out of range.")

    def __setitem__(self, index, value):
        if index >= 0 and index <= 2:
            self.color[index] = value
        raise IndexError("Index out of range.")

if __name__ == "__main__":
    a = Color("FF0000")
    print Color.BLACK()
