import pyglet
from pyglet import gl
import numpy as np

import utility
import datasource as ds


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

    def update(self, dt):
        pass

    def _create_texture(self, width, height, tex_array):
        tex = (gl.GLfloat * len(tex_array))(*tex_array)

        tex_id = gl.GLuint()

        gl.glBindTexture(gl.GL_TEXTURE_2D, tex_id)
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, width, height,
                        0, gl.GL_RGB, gl.GL_FLOAT, tex)

        return tex_id

    def _draw_texture(self, tex_id, x, y, width, height):
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex_id)
        gl.glBegin(gl.GL_QUADS)
        gl.glTexCoord2i(0, 0)
        gl.glVertex2i(x, y)
        gl.glTexCoord2i(1, 0)
        gl.glVertex2i(width, y)
        gl.glTexCoord2i(1, 1)
        gl.glVertex2i(width, height)
        gl.glTexCoord2i(0, 1)
        gl.glVertex2i(x, height)
        gl.glEnd()


class NoiseWidget(AbstractWidget):

    def update(self, dt):
        points = utility.random_points(self._numPoints,
                                       self.width, self.height).tolist()
        self._points = np.ravel(points, order="F").tolist()
        self._colours = utility.random_colours(self._numPoints).tolist()

    def _draw_impl(self):

        pyglet.graphics.draw(self._numPoints, gl.GL_POINTS,
                             ('v2i/stream', self._points),
                             ('c3B/stream', self._colours))


class LinePlotWidget(AbstractWidget):

    def __init__(self, window, x, y, width, height,
                 line_col=(1.0, 1.0, 1.0), data_source=None):
        super().__init__(window, x, y, width, height)

        self._line_col = line_col

        if data_source is None:
            data_source = ds.ConstantDataSource(np.ones(10))

        border_points = (0, 0, 0, self.height, self.width, self.height, self.width, 0)
        self._border = pyglet.graphics.vertex_list(4, ('v2i', border_points))

        self._data_source = data_source
        self._update_data()

    def update(self, dt):
        self._data_source.update(dt)
        self._update_data()

    def _update_data(self):
        data = self._data_source.get_data()
        normed_data = norm_data(data)
        self._update_vertex_list(normed_data)

    def _update_vertex_list(self, normed_data):
        count = normed_data.size
        y_points = (normed_data * self.height)
        x_points = np.linspace(0, self.width, count)
        points = np.stack((x_points, y_points))
        points = np.ravel(points, order="F").tolist()
        self._vertex_list = pyglet.graphics.vertex_list(count, ('v2f', points))

    def _draw_impl(self):
        self._border.draw(gl.GL_LINE_LOOP)
        self._vertex_list.draw(gl.GL_LINE_STRIP)


class HeatmapWidget(AbstractWidget):

    def __init__(self, window, x, y, width, height,
                 min_col=(0.0, 1.0, 0.0), max_col=(1.0, 0.0, 0.0),
                 data_source=None):
        super().__init__(window, x, y, width, height)

        self._minCol = np.array(min_col)
        self._maxCol = np.array(max_col)

        if data_source is None:
            data_source = ds.ConstantDataSource(np.ones((2, 2)))

        self.data_source = data_source

        data = data_source.get_data()
        self.data_width, self.data_height = data.shape
        self._update_texture(data)

    def _update_texture(self, data):
        self._data = data

        normed_data = norm_data(data)

        dataVector = np.ravel(normed_data)
        a = np.outer(self._minCol, (1 - dataVector))
        b = np.outer(self._maxCol, dataVector)
        self._tex_id = self._create_texture(self.data_width, self.data_height,
                                            np.ravel((a + b), order="F"))

    def update(self, dt):
        self.data_source.update(dt)
        data = self.data_source.get_data()
        self._update_texture(data)
        pass

    def _draw_impl(self):

        self._draw_texture(self._tex_id, 0, 0, self.width, self.height)


def norm_data(data):
    min_point = np.amin(data)
    max_point = np.amax(data)

    # If every data point is the same, normalise to 0.5
    if max_point == min_point:
        min_point = 0
        max_point *= 2

    normed_data = (data - min_point) / (max_point - min_point)
    return normed_data


def test():
    pass


if __name__ == '__main__':
    import timeit
    print(1/(timeit.timeit("test()", setup="from __main__ import test", number=10)/10))
