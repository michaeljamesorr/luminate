import numpy as np


def random_points(count, x_max, y_max):
    x_points = np.random.randint(0, x_max, (count))
    y_points = np.random.randint(0, y_max, (count))
    return np.stack((x_points, y_points))


def random_colours(count):
    return np.random.bytes(count*3)
