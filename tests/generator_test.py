import unittest
import numpy as np

import waves.generator as generator


class TestGeneratorMethods(unittest.TestCase):

    def test_random_points(self):
        count = 10
        x_max = 100
        y_max = 200
        points = generator.random_points(count, x_max, y_max)

        self.assertTrue(isinstance(points, np.ndarray))
        self.assertEqual(points.shape, (2, count))
        self.assertTrue(isinstance(points[0][0], int))

    def test_random_colours(self):
        count = 10
        colours = generator.random_colours(count)

        self.assertTrue(isinstance(colours, np.ndarray))
        self.assertEqual(colours.shape, (count*3))
        self.assertTrue(isinstance(colours[0], bytes))
