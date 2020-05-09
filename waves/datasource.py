#!/usr/bin/env python3

import math
import numpy as np
import struct

import cython.cyfilter as sigfilter


class AbstractDataSource:

    has_new_data = True

    def update(self, dt):
        self.has_new_data = self._update_impl(dt)

    def _update_impl(self, dt):
        pass

    def get_data(self):
        self.has_new_data = False
        return self._get_data_impl()

    def _get_data_impl(self):
        pass


class ConstantDataSource(AbstractDataSource):

    def __init__(self, data):
        self._data = data

    def _get_data_impl(self):
        return self._data


class RandomDataSource(AbstractDataSource):

    def __init__(self, data_shape, seed=0):
        super().__init__()

        self._data_shape = data_shape
        self._seed = seed

    def _update_impl(self, dt):
        self._seed += dt
        return True  # new data available

    def _get_data_impl(self):
        np.random.seed(floatToBits(self._seed))
        return np.random.sample(self._data_shape)


class FunctionDataSource(AbstractDataSource):

    def __init__(self, function, var_names, var_ranges, dynamic_var=None, dynamic_var_start=0):
        self._function = function
        self._var_names = var_names
        self._var_ranges = var_ranges
        self._dynamic_var = dynamic_var
        self._dynamic_var_val = dynamic_var_start
        self._sample_point_matrix = self._construct_matrix(var_ranges)

    def _construct_matrix(self, ranges):
        shape = []
        for var_range in ranges:
            shape.append(len(var_range))
        matrix = np.empty(shape, object)

        for idx, val in np.ndenumerate(matrix):
            point = []
            for pos, var_range in enumerate(ranges):
                point.append(var_range[idx[pos]])
            matrix[idx] = point

        return matrix

    def _update_impl(self, dt):
        if self._dynamic_var:
            self._dynamic_var_val += dt
            return True

    def _get_data_impl(self):
        data_matrix = np.zeros(self._sample_point_matrix.shape)

        for idx, sample_point in np.ndenumerate(self._sample_point_matrix):
            kwargs = {}
            for pos, name in enumerate(self._var_names):
                kwargs[name] = sample_point[pos]
            if self._dynamic_var:
                kwargs[self._dynamic_var] = self._dynamic_var_val
            data_matrix[idx] = self._function(**kwargs)

        return data_matrix


def floatToBits(f):
    s = struct.pack('>f', f)
    return struct.unpack('>l', s)[0]


class FilterDataSource(AbstractDataSource):

    def __init__(self, tex_data_2d, kernel_2d):
        self._tex_data = tex_data_2d
        self._kernel = kernel_2d

    def _update_impl(self, dt):
        self._tex_data = sigfilter.apply_filter(self._tex_data, self._kernel)
        return True

    def _get_data_impl(self):
        return self._tex_data


class AudioDataSource(FunctionDataSource):

    def __init__(self, audio_signal, window_length):
        self._audio_signal = audio_signal
        raw_audio = audio_signal.get_array_of_samples()
        # raw_audio = sigfilter.smooth(raw_audio, 22)
        num_samples = len(raw_audio)
        super().__init__(lambda x, t: raw_audio[x + int(t*44000)] if 0 <= x + int(t*44000)
                         and x + int(t*44000) < num_samples else 0, ("x"),
                         [range(window_length)], dynamic_var="t")


def main():
    f_source = FunctionDataSource(lambda x: (math.sin(x)),
                                  ("x"), [np.linspace(-math.pi, math.pi, 20)])
    print(f_source.get_data())


if __name__ == '__main__':
    main()
