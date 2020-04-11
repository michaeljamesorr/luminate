import random


def random_points(count, xMax, yMax):
    points = []
    for _ in range(count):
        points.append(random.randint(0, xMax))
        points.append(random.randint(0, yMax))
    return points


def random_colours(count):
    return bytearray(random.getrandbits(8) for _ in range(count*3))
