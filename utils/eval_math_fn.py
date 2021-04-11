from inspect import getmembers
import numpy as np


def eval_math_fn_at(fn, point):
    return eval_math_fn(fn, {'x': point[0], 'y': point[1]})


def eval_math_fn(function, name_dict):
    math_name_dict = dict(getmembers(np))

    # Uncomment to use custom function
    # x = name_dict['x']
    # y = name_dict['y']
    # return (x ** 2) - y

    return eval(function, {**name_dict, **math_name_dict})
