#!/usr/bin/env python3

import pyglet
from pyglet import gl

import widget
import datasource as ds


class MainApp(pyglet.window.Window):

    _displayFPS = True

    def __init__(self, width, height):
        pyglet.window.Window.__init__(self, width=width, height=height)

        self.widgets = []
        # self.widgets.append(widget.NoiseWidget(self, 100, 100, 100, 100))
        # self.widgets.append(widget.NoiseWidget(self, 300, 300, 100, 100))
        # self.widgets.append(widget.NoiseWidget(self, 500, 500, 200, 100))

        self.widgets.append(widget.HeatmapWidget(self, 100, 100, 1180, 620,
                                                 # (0.0, 0.0, 0.8), (0.0, 0.8, 0.0),
                                                 data_source=ds.RandomDataSource((320, 180))))

        if self._displayFPS:
            self.fps_display = pyglet.window.FPSDisplay(self)

        gl.glEnable(gl.GL_TEXTURE_2D)

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

    def update(self, dt):
        for w in self.widgets:
            w.update(dt)


def main():
    window = MainApp(width=1280, height=720)
    pyglet.clock.schedule_interval(window.update, 0.001)
    pyglet.app.run()


if __name__ == '__main__':
    main()
