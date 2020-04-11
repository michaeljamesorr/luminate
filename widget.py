import pyglet
from pyglet import gl

import numpy as np

import generator


class AbstractWidget:

    _numPoints = 500

    def __init__(self, window, x, y, width, height):
        self._window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):

        gl.glTranslatef(self.x, self.y, 0)

        gl.glPushMatrix()
        self._draw_impl()
        gl.glPopMatrix()

    def _draw_impl(self):
        pass


class NoiseWidget(AbstractWidget):

    def _draw_impl(self):
        points = generator.random_points(self._numPoints,
                                         self.width, self.height)
        colours = generator.random_colours(self._numPoints)

        pyglet.graphics.draw(self._numPoints, gl.GL_POINTS,
                             ('v2i/stream', points),
                             ('c3B/stream', colours))


class HeatmapWidget(AbstractWidget):

    def __init__(self, window, x, y, width, height, minCol, maxCol, data=None):
        super().__init__(window, x, y, width, height)

        self._minCol = np.array(minCol)
        self._maxCol = np.array(maxCol)

        if data is None:
            data = np.array([[np.random.random() for _ in range(height)] for _ in range(width)])

        self._points = []
        for x in range(self.width):
            for y in range(self.height):
                self._points.append(x)
                self._points.append(y)

        self._data = data
        self._generate_texture()

    def update_data(self, data):
        self._data = data
        self._generate_texture()

    def _generate_texture(self):
        min_point = np.amin(self._data)
        max_point = np.amax(self._data)

        normedData = (self._data - min_point) / (max_point - min_point)

        self._tex = [[0 for _ in range(self.height)] for _ in range(self.width)]

        for x in range(self.width):
            for y in range(self.height):
                dataPoint = normedData[x][y]
                self._tex[x][y] = tuple((self._minCol * (1 - dataPoint) + self._maxCol * dataPoint).astype(int))

        colours = []
        for x in range(self.width):
            for y in range(self.height):
                colours.extend(self._tex[x][y])

        self._vertex_list = pyglet.graphics.vertex_list(self.width * self.height,
                                                        ('v2i', self._points),
                                                        ('c3B', colours))

    def _draw_impl(self):

        data = np.array([[np.random.random() for _ in range(self.height)] for _ in range(self.width)])
        self.update_data(data)
        self._vertex_list.draw(gl.GL_POINTS)


def test():
    width = 400
    height = 400

    min_col = (64, 127, 64)
    max_col = (200, 64, 100)

    data = np.array([[np.random.random() for _ in range(height)]for _ in range(width)])
    min_point = np.amin(data)
    max_point = np.amax(data)

    normed_data = (data - min_point) / (max_point - min_point)

    _tex = [[0 for _ in range(height)] for _ in range(width)]

    for x in range(width):
        for y in range(height):
            data_point = normed_data[x][y]
            _tex[x][y] = tuple((min_col * (1 - data_point) + max_col * data_point).astype(int))

    colours = []
    for x in range(width):
        for y in range(height):
            colours.extend(_tex[x][y])
