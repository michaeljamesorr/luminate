#!/usr/bin/env python3

import numpy as np
import struct


class AbstractDataSource:

    def update(self, dt):
        pass

    def get_data(self):
        pass


class ConstantDataSource(AbstractDataSource):

    def __init__(self, data):
        self._data = data

    def get_data(self):
        return self._data


class RandomDataSource(AbstractDataSource):

    def __init__(self, data_shape, seed=0):
        super().__init__()

        self._data_shape = data_shape
        self._seed = seed

    def update(self, dt):
        self._seed += dt

    def get_data(self):
        np.random.seed(floatToBits(self._seed))
        return np.random.sample(self._data_shape)


def floatToBits(f):
    s = struct.pack('>f', f)
    return struct.unpack('>l', s)[0]
