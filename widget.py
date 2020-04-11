import pyglet
from pyglet import gl
import generator
import numpy as np

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
		points = generator.random_points(self._numPoints, self.width, self.height)
		colours = generator.random_colours(self._numPoints)

		pyglet.graphics.draw(self._numPoints, gl.GL_POINTS,
		 ('v2i/stream', points), ('c3B/stream', colours))

class HeatmapWidget(AbstractWidget):
    
    def __init__(self, window, x, y, width, height, minCol, maxCol, data=None):
        super().__init__(window, x, y, width,height)

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
        min = np.amin(self._data)
        max = np.amax(self._data)

        normedData = (self._data - min)/(max-min)

        self._tex = [[0 for _ in range(self.height)] for _ in range(self.width)]

        for x in range(self.width):
            for y in range(self.height):
                dataPoint = normedData[x][y]
                self._tex[x][y] = tuple((self._minCol*(1-dataPoint)+self._maxCol*dataPoint).astype(int))

        colours = []
        for x in range(self.width):
            for y in range(self.height):
                colours.extend(self._tex[x][y])

        self._vertex_list = pyglet.graphics.vertex_list(self.width*self.height,
                            ('v2i', self._points), ('c3B', colours))

    def _draw_impl(self):

        data = np.array([[np.random.random() for _ in range(self.height)] for _ in range(self.width)])
        self.update_data(data)
        self._vertex_list.draw(gl.GL_POINTS)

    

