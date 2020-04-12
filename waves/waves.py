#!/usr/bin/env python3

import math

import numpy as np
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

        # self.widgets.append(widget.HeatmapWidget(self, 100, 100, 1180, 620,
        #                                          # (0.0, 0.0, 0.8), (0.0, 0.8, 0.0),
        #                                          data_source=ds.RandomDataSource((320, 180))))

        func_source = ds.FunctionDataSource(lambda x, t: (math.sin(x-20*t)),
                                            ("x"), [np.linspace(-2*math.pi, 2*math.pi, 100)], dynamic_var="t")
        self.widgets.append(widget.LinePlotWidget(self, 200, 200, 1000, 300,
                                                  data_source=func_source))

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
