

# COLOR TUPLES
def with_alpha(alpha, color_tuple):
    """
    convert color so it has an alpha channel
    :param alpha: alpha channel to add to color tuple
    :param color_tuple: color to convert
    :return: color with an alpha channel
    """
    list_color = list(color_tuple)
    list_color.append(alpha)
    return tuple(list_color)


class Color:
    transparent = (0, 0, 0, 0)
    null = transparent
    nothing = transparent
    blank = transparent

    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    cyan = (0, 255, 255)
    yellow = (255, 255, 0)


color = Color()
