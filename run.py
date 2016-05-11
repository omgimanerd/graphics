#!/usr/bin/python
# This takes an mdl file, compiles it, and runs the commands contained in it.
# Author: alvin.lin.dev@gmail.com (Alvin Lin)

import graphics.compiler.mdl as mdl

from graphics.lib.color import Color
from graphics.lib.drawing import Drawing
from graphics.lib.generator import Generator
from graphics.lib.matrix import Matrix, TransformationMatrix, EdgeMatrix
from graphics.lib.util import Util

import argparse
import traceback

class Runner():

    DEFAULT_FRAMECOUNT = 60

    def __init__(self, width=512, height=512, color="#FF0000",
                 directory="", verbose=False):
        """
        Constructor for the Runner class.

        Parameters:
        width: int (optional), the width of the image to generate
        height: int (optional), the height of the image to generate
        color: string (optional), the hexadecimal representation of the color to
            use when drawing
        """
        self.width = width
        self.height = height
        self.drawing = Drawing(width, height)
        self.color = Color(color)
        self.directory = directory
        self.verbose = verbose

        self.frames = Runner.DEFAULT_FRAMECOUNT
        self.basename = "%s/default_basename" % self.directory.strip("/")
        self.knobs = {}

    def set_frames(self, frames):
        """
        Sets the framecount of the animation.

        Parameters:
        frames: int, the number of frames in the animation
        """
        self.frames = frames

    def set_basename(self, basename):
        """
        Sets the basename of the animation frames.

        Parameters:
        basename: str, the basename of the animation frames
        """
        self.basename = "%s/%s" % (self.directory.strip("/"), basename)

    def set_knob(self, knob_name, from_frame, to_frame, from_value, to_value):
        """
        Sets a variable knob in the animation.

        Parameters:
        knob_name: str, the name of the knob
        from_frame: int, the frame that this knob starts changing at
        to_frame: int, the frame that this knob stops changing at
        from_value: int, the value that this knob starts at
        to_value: int, the value that this knob stops at
        """
        if knob_name in self.knobs:
            self.knobs[knob_name] = [0 for x in range(self.frames)]
        else:
            self.knobs[knob_name] = Generator.get_knob_range(
                self.frames, from_frame, to_frame, from_value, to_value)

    def run(self, filename):
        """
        Reads the given file, compiles the code found in it, and runs it.

        Parameters:
        filename: str, the name of the file to read from
        """
        animation_commands = {
            "frames": self.set_frames,
            "basename": self.set_basename,
            "vary": self.set_knob
        }
        variable_commands = {
            "rotate": self.drawing.rotate,
            "translate": self.drawing.translate,
            "move": self.drawing.translate,
            "scale": self.drawing.scale
        }
        # Represents the index of the parameters that should be affected by
        # the vary commands.
        scaled_parameter_indices = {
            "rotate": [1],
            "translate": [0, 1, 2],
            "move": [0, 1, 2],
            "scale": [0, 1, 2]
        }
        drawing_commands = {
            "push": self.drawing.push_matrix,
            "pop": self.drawing.pop_matrix,
            "identity": self.drawing.identity,
            "line": self.drawing.draw_line,
            "circle": self.drawing.draw_circle,
            "hermite": self.drawing.draw_hermite_curve,
            "bezier": self.drawing.draw_bezier_curve,
            "box": self.drawing.draw_box,
            "sphere": self.drawing.draw_sphere,
            "torus": self.drawing.draw_torus,
            "display": self.drawing.display,
            "save": self.drawing.generate
        }
        commands = None
        symbols = None
        try:
            (commands, symbols) = mdl.parseFile(filename)
        except:
            print "Parsing failed."
            print traceback.format_exc()
            return

        try:
            for command in commands:
                name = command[0]
                if name in animation_commands:
                    args = command[1:]
                    animation_commands[name](*args)
        except:
            print "Animation commands invalid!"
            print traceback.format_exc()
            return

        try:
            if self.knobs:
                del drawing_commands["save"]
                for frame in range(self.frames):
                    for command in commands:
                        name = command[0]
                        args = list(command[1:-1])
                        knob = command[-1]
                        if name in variable_commands:
                            if knob:
                                for index in scaled_parameter_indices[name]:
                                    args[index] *= self.knobs[knob][frame]
                            variable_commands[name](*args)
                        elif name in drawing_commands:
                            drawing_commands[name](*args)
                    filename = "%s_%s" % (self.basename, str(frame).zfill(
                        len(str(self.frames))))
                    self.drawing.generate(filename)
                    self.drawing.clear()
                    if self.verbose:
                        print "Generated %s" % filename
            else:
                for command in commands:
                    name = command[0]
                    args = command[1:-1]
                    functions = Util.merge_dicts(variable_commands,
                                                drawing_commands)
                    if name in functions:
                        functions[name](*args)
        except:
            print "Execution failed."
            print traceback.format_exc()
            return


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("file", help="The mdl file to run")
    argparser.add_argument("--verbose", action="store_true")
    argparser.add_argument("--dir", type=str, default=".")
    args = argparser.parse_args()

    runner = Runner(directory=args.dir, verbose=args.verbose)
    runner.run(args.file)
