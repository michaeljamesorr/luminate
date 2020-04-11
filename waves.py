#!/usr/bin/env python3

import pyglet
from pyglet import gl
import random
from widget import *


class MainApp(pyglet.window.Window):

	_displayFPS = True

	def __init__(self, width, height):
		pyglet.window.Window.__init__(self, width=width, height=height)

		self.widgets = []
		self.widgets.append(NoiseWidget(self, 100, 100, 100, 100))
		self.widgets.append(NoiseWidget(self, 300, 300, 100, 100))
		self.widgets.append(NoiseWidget(self, 500, 500, 200, 100))

		if self._displayFPS:
			self.fps_display = pyglet.window.FPSDisplay(self)

	def on_draw(self):
		self.clear()

		if self._displayFPS:
			self.fps_display.draw()

		gl.glMatrixMode(gl.GL_MODELVIEW)
		gl.glLoadIdentity()

		for w in self.widgets:
			gl.glPushMatrix()
			w.draw()
			gl.glPopMatrix()

def update(dt):
	pass

def main():
	MainApp(width=1280, height=720)
	pyglet.clock.schedule_interval(update, 0.01)
	pyglet.app.run()



if __name__ == '__main__':
	main()