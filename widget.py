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

    data_width = 320
    data_height = 180

    def __init__(self, window, x, y, width, height, minCol, maxCol, data=None):
        super().__init__(window, x, y, width, height)

        self._minCol = np.array(minCol)
        self._maxCol = np.array(maxCol)

        if data is None:
            data = np.random.rand(self.data_width, self.data_height)

        self._data = data
        self._generate_texture()

    def update_data(self, data):
        self._data = data
        self._generate_texture()

    def _generate_texture(self):
        min_point = np.amin(self._data)
        max_point = np.amax(self._data)

        normed_data = (self._data - min_point) / (max_point - min_point)

        dataVector = np.ravel(normed_data)
        a = np.outer(self._minCol, (1 - dataVector))
        b = np.outer(self._maxCol, dataVector)
        self._tex = np.ravel((a + b), order="F")

        self._tex = (gl.GLfloat * len(self._tex))(*self._tex)

        self._tex_id = gl.GLuint()

        gl.glBindTexture(gl.GL_TEXTURE_2D, self._tex_id)
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, self.data_width, self.data_height,
                        0, gl.GL_RGB, gl.GL_FLOAT, self._tex)

    def _draw_impl(self):

        data = np.random.rand(self.data_width, self.data_height)
        self.update_data(data)

        gl.glBindTexture(gl.GL_TEXTURE_2D, self._tex_id)
        gl.glBegin(gl.GL_QUADS)
        gl.glTexCoord2i(0, 0)
        gl.glVertex2i(0, 0)
        gl.glTexCoord2i(1, 0)
        gl.glVertex2i(self.width, 0)
        gl.glTexCoord2i(1, 1)
        gl.glVertex2i(self.width, self.height)
        gl.glTexCoord2i(0, 1)
        gl.glVertex2i(0, self.height)
        gl.glEnd()


def test():
    pass


if __name__ == '__main__':
    import timeit
    print(1/(timeit.timeit("test()", setup="from __main__ import test", number=10)/10))
