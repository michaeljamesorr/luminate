import unittest
import numpy as np

import waves.utility


class TestUtilityFunctions(unittest.TestCase):

    def test_random_points(self):
        count = 10
        x_max = 100
        y_max = 200
        points = waves.utility.random_points(count, x_max, y_max)

        self.assertTrue(isinstance(points, np.ndarray))
        self.assertEqual(points.shape, (2, count))

    def test_random_colours(self):
        count = 10
        colours = waves.utility.random_colours(count)

        self.assertTrue(isinstance(colours, bytes))
        self.assertEqual(len(colours), count*3)
