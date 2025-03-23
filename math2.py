# Some much needed functions that for some reason aren't part of built-in math library

def clamp(value, lower, upper):
    return lower if value < lower else upper if value > upper else value

def lerp(a: float, b: float, alpha: float) -> float:
    """https://gist.github.com/laundmo/b224b1f4c8ef6ca5fe47e132c8deab56
    Linear interpolate on the scale given by a to b, using alpha as the point on that scale.
    Examples
    --------
        50 == lerp(0, 100, 0.5)
        4.2 == lerp(1, 5, 0.8)
    """
    return (1 - alpha) * a + alpha * b

def map_range_clamped(value, in_min, in_max, out_min, out_max):
    """
    Maps a value from one range to another while clamping it to the input range.

    :param value: float - The input value to be mapped.
    :param in_min: float - The minimum value of the input range.
    :param in_max: float - The maximum value of the input range.
    :param out_min: float - The minimum value of the output range.
    :param out_max: float - The maximum value of the output range.
    :return: float - The mapped and clamped value in the output range.
    """
    # Clamp the value within the input range
    clamped_value = clamp(value, in_min, in_max)

    # Normalize and map the value to the output range
    return out_min + (clamped_value - in_min) * (out_max - out_min) / (in_max - in_min)