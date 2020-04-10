#!/usr/bin/env python3

import pyglet
from pyglet import gl
import random

class MainApp(pyglet.window.Window):

	_displayFPS = True
	_numPoints = 5000

	def __init__(self, width, height):
		pyglet.window.Window.__init__(self, width=width, height=height)

		if self._displayFPS:
			self.fps_display = pyglet.window.FPSDisplay(self)

	def on_draw(self):
		self.clear()

		if self._displayFPS:
			self.fps_display.draw()
			
		gl.glPushMatrix()
		gl.glMatrixMode(gl.GL_MODELVIEW)
		gl.glLoadIdentity()
		gl.glTranslatef(100.0, 100.0, 0)

		points = random_points(self._numPoints, self.width, self.height)
		colours = random_colours(self._numPoints)
		pyglet.graphics.draw(self._numPoints, gl.GL_POINTS,
		 ('v2i/stream', points), ('c3B/stream', colours))

		gl.glPopMatrix()

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