#!/usr/bin/env python3

import pyglet
from pyglet import gl
import numpy as np
# import cv2

import widget
import cython.cyfilter as sigfilter

import datasource as ds


class MainApp(pyglet.window.Window):

    _displayFPS = True

    def __init__(self, width, height):
        pyglet.window.Window.__init__(self, width=width, height=height)

        self.widgets = []
        # self.widgets.append(widget.NoiseWidget(self, 100, 100, 100, 100))
        # self.widgets.append(widget.NoiseWidget(self, 300, 300, 100, 100))
        # self.widgets.append(widget.NoiseWidget(self, 500, 500, 200, 100))

        # tex_data = np.zeros((height, width, 3))
        # tex_data[::30, :, :] = 1
        # tex_data[:, ::30, :] = 1

        # img = cv2.imread("data/DSC_1446.jpg")
        # tex_data = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # tex_data = tex_data.astype(float)/255
        # tex_data = sigfilter.sobel_edge_detect(tex_data)

        tex_data = np.zeros((200, 200, 3))
        tex_data[50, :, :] = (1.0, 0.0, 0.0)
        tex_data[100, :, :] = (0.0, 0.0, 1.0)
        tex_data[150, :, :] = (0.0, 1.0, 0.0)

        self.widgets.append(widget.TextureWidget(self, 0, 0, width, height,
                            data_source=ds.FilterDataSource(tex_data, sigfilter.FLOW)))

        # self.widgets.append(widget.HeatmapWidget(self, 100, 100, 1180, 620,
        #                                          # (0.0, 0.0, 0.8), (0.0, 0.8, 0.0),
        #                                          data_source=ds.RandomDataSource((320, 180))))

        # func_source = ds.FunctionDataSource(lambda x, t: (math.sin(x-20*t)),
        #                                     ("x"), [np.linspace(-2*math.pi, 2*math.pi, 100)], dynamic_var="t")
        # audio_signal = AudioSegment.from_file("data/test_audio.m4a", "m4a")
        # normed_signal = pydub.effects.normalize(audio_signal)
        # normed_signal = normed_signal[:20000][-18000:]
        # split_audio = normed_signal.split_to_mono()
        # # mono_audio = split_audio[0].overlay(split_audio[1])
        # raw_signal = split_audio[0].get_array_of_samples()
        # # smoothed_signal = sigfilter.smooth(raw_signal[:440000], 220)
        # # audio_source = ds.AudioDataSource(split_audio[0][:10000], 1)
        # # self.widgets.append(widget.LinePlotWidget(self, 0, 0, 1280, 300,
        # #                                           data_source=audio_source))

        # func_source = ds.FunctionDataSource(lambda x, y, t: (raw_signal[int(y) + int(t*440)]+math.sin(x)),
        #                                     ("x", "y"),
        #                                     [np.linspace(-2*math.pi, 2*math.pi, 100),
        #                                      np.linspace(0, 440, 100)],
        #                                     dynamic_var="t")
        # self.widgets.append(widget.HeatmapWidget(self, 0, 0, 1280, 720,
        #                                          (0.0, 0.0, 0.8), (0.0, 0.8, 0.0),
        #                                          data_source=func_source))

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
    window = MainApp(width=800, height=800)
    pyglet.clock.schedule_interval(window.update, 0.001)
    pyglet.app.run()


if __name__ == '__main__':
    main()
