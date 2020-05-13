import numpy as np


def random_points(count, x_max, y_max):
    x_points = np.random.randint(0, x_max, (count))
    y_points = np.random.randint(0, y_max, (count))
    return np.stack((x_points, y_points))


def random_colour_bytes(count):
    return np.random.bytes(count*3)


def random_colour_floats(count):
    return np.random.uniform(size=count*3).reshape((count, 3))


def hsv_to_rgb(h, s, v):
    if s == 0.0:
        return (v, v, v)
    i = int(h*6.)
    f = (h*6.)-i
    p, q, t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f))
    i %= 6
    if i == 0:
        return (v, t, p)
    if i == 1:
        return (q, v, p)
    if i == 2:
        return (p, v, t)
    if i == 3:
        return (p, q, v)
    if i == 4:
        return (t, p, v)
    if i == 5:
        return (v, p, q)


def split_complementary_color_palette(h, s, v):
    palette = []
    palette.append((h, s, v))
    palette.append(((h + 0.45) % 1, s, v))
    palette.append(((h + 0.55) % 1, s, v))
    return palette


def triadic_color_palette(h, s, v):
    palette = []
    for i in range(3):
        h_i = (h + i/3) % 1
        palette.append((h_i, s, v))
    return palette
