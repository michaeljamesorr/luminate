#!/usr/bin/env python3

import pyglet
from pyglet import gl
import random

class AbstractWidget:


	_numPoints = 5000

	def __init__(self, window, x, y, width, height):
		self._window = window
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def draw(self):
		gl.glPushMatrix()
		gl.glMatrixMode(gl.GL_MODELVIEW)
		gl.glLoadIdentity()
		gl.glTranslatef(self.x, self.y, 0)

		self._draw_impl()

		gl.glPopMatrix()

	def _draw_impl(self):
		pass

class NoiseWidget(AbstractWidget):

	def _draw_impl(self):
		points = random_points(self._numPoints, self.width, self.height)
		colours = random_colours(self._numPoints)
		pyglet.graphics.draw(self._numPoints, gl.GL_POINTS,
		 ('v2i/stream', points), ('c3B/stream', colours))

class MainApp(pyglet.window.Window):

	_displayFPS = True

	def __init__(self, width, height):
		pyglet.window.Window.__init__(self, width=width, height=height)

		self.widgets = []
		self.widgets.append(NoiseWidget(self, 100, 100, 100, 100))

		if self._displayFPS:
			self.fps_display = pyglet.window.FPSDisplay(self)

	def on_draw(self):
		self.clear()

		if self._displayFPS:
			self.fps_display.draw()

		for w in self.widgets:
			w.draw()


def random_points(count, xMax, yMax):
	points = []
	for _ in range(count):
		points.append(random.randint(0, xMax))
		points.append(random.randint(0, yMax))
	return points

def random_colours(count):
	return bytearray(random.getrandbits(8) for _ in range(count*3))

def update(dt):
	pass

def main():
	MainApp(width=1280, height=720)
	pyglet.clock.schedule_interval(update, 0.01)
	pyglet.app.run()



if __name__ == '__main__':
	main()