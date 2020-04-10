#!/usr/bin/env python3

import pyglet

window = pyglet.window.Window()

label = pyglet.text.Label('Hello world', x=window.width//2, y=window.height//2)

def main():
	pyglet.app.run()
	

@window.event
def on_draw():

	window.clear()
	label.draw()

	pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (10, 15, 30, 35)))



if __name__ == '__main__':
	main()