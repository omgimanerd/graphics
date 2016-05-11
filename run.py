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
        # These objects store link the mdl function with the internal function
        # and store the number of parameters each function requires.
        animation_commands = {
            "frames": { "function": self.set_frames, "params": 1 },
            "basename": { "function": self.set_basename, "params": 1 },
            "vary": { "function": self.set_knob, "params": 5 }
        }
        variable_commands = {
            "rotate": { "function": self.drawing.rotate, "params": 2,
                        "indices": [1] },
            "move": { "function": self.drawing.translate, "params": 3,
                      "indices": [0, 1, 2] },
            "scale": { "function": self.drawing.scale, "params": 3,
                       "indices": [0, 1, 2] }
        }
        drawing_commands = {
            "push": { "function": self.drawing.push_matrix, "params": 0 },
            "pop": { "function": self.drawing.pop_matrix, "params": 0 },
            "identity": { "function": self.drawing.identity, "params": 0 },
            "line": { "function": self.drawing.draw_line, "params": 6 },
            "circle": { "function": self.drawing.draw_circle, "params": 3 },
            "hermite": { "function": self.drawing.draw_hermite_curve,
                         "params": 8 },
            "bezier": { "function": self.drawing.draw_bezier_curve,
                        "params": 8 },
            "box": { "function": self.drawing.draw_box, "params": 6 },
            "sphere": { "function": self.drawing.draw_sphere, "params": 4 },
            "torus": { "function": self.drawing.draw_torus, "params": 5 },
            "display": { "function": self.drawing.display, "params": 0 },
            "save": { "function": self.drawing.generate, "params": 1 }
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
                    args = command[1:][:animation_commands[name]["params"]]
                    animation_commands[name]["function"](*args)
        except:
            print "Animation commands invalid!"
            print traceback.format_exc()
            return

        try:
            if self.knobs:
                # If we are animating, then save is no longer a valid command.
                del drawing_commands["save"]
                for frame in range(self.frames):
                    for command in commands:
                        name = command[0]
                        # If the command is a matrix transformation that a
                        # varying knob can be applied to, then modify the
                        # appropriate argument with the vary amount. The
                        # position of the argument to vary is stored in
                        # the variable_commands dictionary under the key
                        # indices for each variable command.
                        if name in variable_commands:
                            knob = command[-1]
                            args = list(command[1:-1])
                            if knob:
                                for index in variable_commands[name]["indices"]:
                                    args[index] *= self.knobs[knob][frame]
                            variable_commands[name]["function"](*args)
                        # Otherwise, if the command is a drawing command,
                        # isolate the necessary parameters and run it.
                        elif name in drawing_commands:
                            args = command[1:][
                                :drawing_commands[name]["params"]]
                            drawing_commands[name]["function"](*args)
                    # Generate an image file for each frame.
                    filename = "%s_%s" % (self.basename, str(frame).zfill(
                        len(str(self.frames))))
                    self.drawing.generate(filename)
                    self.drawing.clear()
                    if self.verbose:
                        print "Generated %s" % filename
            else:
                # If we are not animating, then just run all the commands.
                for command in commands:
                    name = command[0]
                    if name in variable_commands:
                        args = command[1:-1]
                        variable_commands[name]["function"](*args)
                    elif name in drawing_commands:
                        # This line extracts the necessary parameters from the
                        # command by checking how many parameters this function
                        # takes.
                        args = command[1:][:drawing_commands][name]["params"]
                        drawing_commands[name](*args)
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
