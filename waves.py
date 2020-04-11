#!/usr/bin/env python3

import pyglet
from pyglet import gl
import widget


class MainApp(pyglet.window.Window):

    _displayFPS = True

    def __init__(self, width, height):
        pyglet.window.Window.__init__(self, width=width, height=height)

        self.widgets = []
        # self.widgets.append(widget.NoiseWidget(self, 100, 100, 100, 100))
        # self.widgets.append(widget.NoiseWidget(self, 300, 300, 100, 100))
        # self.widgets.append(widget.NoiseWidget(self, 500, 500, 200, 100))

        self.widgets.append(widget.HeatmapWidget(self, 0, 0, 1280, 720, (0, 0, 200), (0, 200, 0)))

        if self._displayFPS:
            self.fps_display = pyglet.window.FPSDisplay(self)

    def on_draw(self):
        self.clear()

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        for w in self.widgets:
            gl.glPushMatrix()
            w.draw()
            gl.glPopMatrix()

        if self._displayFPS:
            self.fps_display.draw()


def update(dt):
    pass


def main():
    MainApp(width=1280, height=720)
    pyglet.clock.schedule_interval(update, 0.001)
    pyglet.app.run()


if __name__ == '__main__':
    main()
