#!/usr/bin/env python3

import pyglet
import random

class MainApp(pyglet.window.Window):

	displayFPS = True

	def __init__(self, width, height):
		pyglet.window.Window.__init__(self, width=width, height=height)
		self.numPoints = 5000
		random.seed(0)

		if self.displayFPS:
			self.fps_display = pyglet.window.FPSDisplay(self)

	def on_draw(self):
		self.clear()
		if self.displayFPS:
			self.fps_display.draw()

		points = random_points(self.numPoints, self.width, self.height)
		colours = random_colours(self.numPoints)
		pyglet.graphics.draw(self.numPoints, pyglet.gl.GL_POINTS,
		 ('v2i/stream', points), ('c3B/stream', colours))

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