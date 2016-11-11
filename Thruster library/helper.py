# Contains helper functions used in main
from math import atan


def angle(x, y):
    """ Returns angle that the joystick makes with the origin

    Arguments:
    x -- x value of the joystick
    y -- y value of the joystick

    Returns:
    Angle in degrees
    """
    if x == 0:
        if y < 0:
            return 270
        if y > 0:
            return 90
        else:
            return 0
    tan = y / x
    arctan = atan(tan) / 3.14 * 180
    if x > 0 and y >= 0:
        return arctan
    elif x > 0 and y < 0:
        return arctan + 360
    elif x < 0 and y <= 0:
        return arctan + 180
    elif x < 0 and y > 0:
        arctan + 180


def map(val, in_min, in_max, out_min, out_max):
    """ Maps value within given range to a different range

    Arguments:
    val -- value to be mapped
    in_min -- lower bound of the val
    in_max -- upper bound of the val
    out_min -- lower bound of the new range
    out_max -- upper bound of the new range

    Returns:
    Value mapped to a different range
    """
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
