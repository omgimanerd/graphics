#!/usr/bin/python
# This file contains decorator functions used by the rest of the graphics
# engine.
# Author: alvin.lin.dev@gmail.com (Alvin Lin)

from functools import wraps
from time import time

def accepts(*arg_types):
    """
    This decorator allows for type checking to ensure that our we pass
    the correct Matrix or Vector into our shit.

    Parameters:
    *args, the argument types for the function that this decorator will wrap

    Example usage:
    @accepts(list, int, set)
    def foo(a, b, c):
        ...
    a must be a list
    b must be an int
    c must be a set

    @accepts((list, int), int, set)
    def bar(a, b, c):
        ...
    a can be of type list or int
    b must be an int
    c must be a set
    """
    def wrapper(fn):
        @wraps(fn)
        def wrapped_fn(*args, **kwargs):
            if len(arg_types) != len(args):
                raise TypeError("%s takes exactly %d arguments (%d given)" % (
                    fn.func_name, len(arg_types), len(args)
                ))
            for i, arg_type in enumerate(arg_types):
                if (isinstance(arg_type, (list, set)) and (
                    not isinstance(args[i], arg_type))):
                        raise TypeError("%s is not of types" % (
                            arg[i], arg_type
                        ))
                elif not isinstance(args[i], arg_types[i]):
                    raise TypeError("%s is not of type %s" % (
                        args[i], arg_types[i]
                    ))
            return fn(*args, **kwargs)
        return wrapped_fn
    return wrapper

def debug(fn):
    @wraps(fn)
    def wrapped_fn(*args, **kwargs):
        start_time = time()
        print "%s%s" % (fn.func_name, args)
        result = fn(*args, **kwargs)
        print "Runtime: %s" % (time() - start_time)
        return result
    return wrapped_fn


if __name__ == "__main__":
    @debug
    @accepts(int, float)
    def foo(a, b):
        pass

    @debug
    @accepts((list, set), int)
    def bar(a, b):
        pass

    from color import Color

    @accepts(Color)
    def baz(a):
        print a

    baz(Color("445566"))
