
#cython: language_level=3

# distutils: extra_compile_args=-fopenmp
# distutils: extra_link_args=-fopenmp

import array
import numpy as np

cimport cython

DTYPE = np.float64

GAUSS_BLUR_3 = np.array((1, 2, 1, 2, 4, 2, 1, 2, 1)).reshape((3, 3))/16
SIMPLE_EDGE_DETECT = np.array((-1, -1, -1, -1, 8, -1, -1, -1, -1)).reshape((3, 3)).astype(float)
SOBEL_EDGE_X = np.array((1, 0, -1, 2, 0, -2, 1, 0, -1)).reshape((3, 3)).astype(float)
SOBEL_EDGE_Y = np.array((1, 2, 1, 0, 0, 0, -1, -2, -1)).reshape((3, 3)).astype(float)

def sobel_edge_detect(double[:,:,:] tex_2d):
    G_x = apply_filter(tex_2d, SOBEL_EDGE_X)
    G_y = apply_filter(tex_2d, SOBEL_EDGE_Y)
    return np.sqrt(np.square(G_x)+np.square(G_y))

def average_kernel(int radius):
    diameter = 2 * radius + 1
    size = diameter ** 2

    return np.full((diameter, diameter), 1.0/size)

@cython.boundscheck(False)
@cython.wraparound(False)
def apply_filter(double[:,:,::1] tex_2d, double[:,::1] kernel_2d):

    cdef Py_ssize_t tex_x_len = tex_2d.shape[0]
    cdef Py_ssize_t tex_y_len = tex_2d.shape[1]

    cdef Py_ssize_t kern_i_radius = int((kernel_2d.shape[0] - 1)/2)
    cdef Py_ssize_t kern_j_radius = int((kernel_2d.shape[1] - 1)/2)

    result = np.zeros((tex_x_len, tex_y_len, 3))
    cdef double[:,:,:] result_view = result

    cdef double[:] acc = np.zeros((3))
    cdef Py_ssize_t x, y, i, j, k

    for x in range(tex_x_len):
        for y in range(tex_y_len):
            acc[:] = 0
            for i in range(-kern_i_radius, kern_i_radius+1):
                for j in range(-kern_j_radius, kern_j_radius+1):
                    if x + i >= 0 and x + i < tex_x_len and y + j >= 0 and y + j < tex_y_len:
                        for k in range(len(acc)):
                            acc[k] += tex_2d[x+i, y+j, k]*kernel_2d[kern_i_radius+i, kern_j_radius+j]
            result_view[x, y, :] = acc

    return result


def smooth(data, N):

    output = array.array('d', data)
    for idx, val in enumerate(data):
        data_sum = 0
        for n in range(-N, N):
            if 0 <= idx + n and idx + n < len(data):
                data_sum += data[idx+n]
        output[idx] = data_sum/(2*N+1)

    return output
