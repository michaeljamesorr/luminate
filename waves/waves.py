#!/usr/bin/env python3

# import random

import pyglet
from pyglet import gl
import numpy as np
import cv2

import widget
import cython.cyfilter as sigfilter
import cython.cydraw as draw
import datasource as ds
import utility


class MainApp(pyglet.window.Window):

    _displayFPS = False

    def __init__(self, width, height):
        pyglet.window.Window.__init__(self, width=width, height=height)

        self.widgets = []
        # self.widgets.append(widget.NoiseWidget(self, 100, 100, 100, 100))
        # self.widgets.append(widget.NoiseWidget(self, 300, 300, 100, 100))

        # tex_data = np.zeros((700, 600, 3))
        # tex_data[::30, :, :] = 1
        # tex_data[:, ::30, :] = 1

        img = cv2.imread("data/DSC_2665.jpg")
        tex_data = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        tex_data = tex_data.astype(float)/255

        tex_scaled = sigfilter.nearest_neighbour_scale(tex_data, 432, 540)
        # tex_data = sigfilter.nearest_neighbour_scale(tex_data, 1080, 1080)
        # tex_data = sigfilter.apply_filter(tex_data, sigfilter.GAUSS_BLUR_3)
        tex_grey = sigfilter.convert_grayscale(tex_scaled)
        tex_edges = sigfilter.sobel_edge_detect(tex_grey)
        tex_edges = tex_edges ** 0.3
        tex_edges *= 1/np.max(tex_edges)
        # print(np.histogram(tex_edges, bins=256))
        tex_threshold = sigfilter.onebit_posterize(tex_edges, 0.65)
        # tex_threshold = sigfilter.binary_thinning(tex_threshold)
        # tex_threshold = sigfilter.binary_dilation(tex_threshold)
        # tex_threshold = sigfilter.binary_erosion(tex_threshold)
        # tex_edges = sigfilter.apply_filter(tex_edges, sigfilter.GAUSS_BLUR_5)
        # tex_edges = sigfilter.apply_filter(tex_edges, sigfilter.GAUSS_BLUR_5)
        tex_mask = tex_threshold + tex_edges
        tex_mask = np.clip(tex_mask, 0.0, 1.0)
        tex_mask = sigfilter.apply_filter(tex_mask, sigfilter.GAUSS_BLUR_5)
        tex_mask = 1 - tex_mask

        tex_data = np.zeros((540, 432, 3))

        points = np.ravel(utility.random_points(20, 432, 540), order="F").reshape(20, 2)
        palette = utility.split_complementary_color_palette(0.055, 0.7, 0.7)

        for i in range(0, 20, 2):
            draw.plot_line(tex_data, points[i, 0], points[i, 1], points[i+1, 0], points[i+1, 1],
                           np.array(utility.hsv_to_rgb(*palette[i % 3])))

        self.widgets.append(widget.TextureWidget(self, 0, 0, width, height, alpha=1.0,
                            data_source=ds.FilterDataSource(tex_data, sigfilter.FLOW_3,
                                                            strength_mask=tex_mask,
                                                            cutoff=0.7)))
        # self.widgets.append(widget.TextureWidget(self, 0, 0, width, height, alpha=0.7,
        #                     data_source=ds.ConstantDataSource(tex_data)))

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

        if self._displayFPS:
            self.fps_display.draw()

    def update(self, dt):
        for w in self.widgets:
            w.update(dt)


def main():
    window = MainApp(width=864, height=1080)
    pyglet.clock.schedule_interval(window.update, 0.001)
    pyglet.app.run()


if __name__ == '__main__':
    main()
