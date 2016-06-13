#!/usr/bin/python
# Author: Alvin Lin (alvin.lin.dev@gmail.com)
# This is a class that manages light values with ambient and point lights.

class Light:

    def __init__(self):
        """
        Constructor for the Light class.
        """
        self.i_ambient = None
        self.i_diffuse = None
        self.i_specular = None

    def get_illumination(self):
        return self.i_ambient + self.i_diffuse + self.i_specular

    def set_ambient_light(self, color, kA):
        self.i_ambient = color * kA

    def set_diffuse_light(self, color, kD, angle):
        pass


if __name__ == "__main__":
    pass
