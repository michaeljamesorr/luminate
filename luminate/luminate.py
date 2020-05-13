#!/usr/bin/env python3

import pyglet
from pyglet import gl


class MainApp(pyglet.window.Window):

    _running = False

    _display_fps = False
    widgets = []

    def __init__(self, width, height, display_fps=False):
        pyglet.window.Window.__init__(self, width=width, height=height)
        self._display_fps = display_fps

        if self._display_fps:
            self.fps_display = pyglet.window.FPSDisplay(self)

        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_REPLACE)

    def on_draw(self):
        self.clear()

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        for w in self.widgets:
            gl.glPushMatrix()
            w.draw()
            gl.glPopMatrix()

        if self._display_fps:
            self.fps_display.draw()

    def update(self, dt):
        for w in self.widgets:
            w.update(dt)

    def run(self):
        if not self._running:
            pyglet.clock.schedule_interval(self.update, 0.001)
            pyglet.app.run()
            self._running = True


def main():
    import utility
    import widget
    import datasource
    window = MainApp(width=800, height=600)
    test_tex = datasource.ConstantDataSource(utility.get_test_pattern())
    window.widgets.append(widget.TextureWidget(window, 0, 0, 800, 600, data_source=test_tex))
    window.run()


if __name__ == '__main__':
    main()
