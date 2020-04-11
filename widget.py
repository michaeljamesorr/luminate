import pyglet
from pyglet import gl
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
		points = generator.random_points(self._numPoints, self.width, self.height)
		colours = generator.random_colours(self._numPoints)

		pyglet.graphics.draw(self._numPoints, gl.GL_POINTS,
		 ('v2i/stream', points), ('c3B/stream', colours))