
#cython: language_level=3

import array
import numpy as np

cimport cython
from libc.math cimport floor

GAUSS_BLUR_3 = np.array((1, 2, 1, 2, 4, 2, 1, 2, 1)).reshape((3, 3))/16
GAUSS_BLUR_5 = np.array((1, 4, 6, 4, 1,
                   4, 16, 24, 16, 4,
                   6, 24, 36, 24, 6,
                   4, 16, 24, 16, 4,
                   1, 4, 6, 4, 1)).reshape((5,5))/256
SIMPLE_EDGE_DETECT = np.array((-1, -1, -1, -1, 8, -1, -1, -1, -1)).reshape((3, 3)).astype(float)
SOBEL_EDGE_X = np.array((1, 0, -1, 2, 0, -2, 1, 0, -1)).reshape((3, 3)).astype(float)
SOBEL_EDGE_Y = np.array((1, 2, 1, 0, 0, 0, -1, -2, -1)).reshape((3, 3)).astype(float)

FLOW_3 = np.array((1, 2, 1, 2, 4, 2, 1, 2, 1)).reshape((3, 3))/6
FLOW_5 = np.array((1, 4, 6, 4, 1,
                   4, 16, 24, 16, 4,
                   6, 24, 36, 24, 6,
                   4, 16, 24, 16, 4,
                   1, 4, 6, 4, 1)).reshape((5,5))/224

def nearest_neighbour_scale(tex_2d, int width, int height):
    cdef double x_scale = tex_2d.shape[1] / width
    cdef double y_scale = tex_2d.shape[0] / height

    new_shape = list(tex_2d.shape)
    new_shape[0] = height
    new_shape[1] = width

    result = np.zeros(new_shape)

    cdef Py_ssize_t x, y, i, j

    for y in range(height):
        for x in range(width):
            i = int(floor((x + 0.5) * x_scale))
            j = int(floor((y + 0.5) * y_scale))
            result[y, x, :] = tex_2d[j, i, :]

    return result

def sobel_edge_detect(double[:,:,:] tex_2d):
    G_x = apply_filter(tex_2d, SOBEL_EDGE_X)
    G_y = apply_filter(tex_2d, SOBEL_EDGE_Y)
    return np.sqrt(np.square(G_x)+np.square(G_y))

def average_kernel(int radius):
    diameter = 2 * radius + 1
    size = diameter ** 2

    return np.full((diameter, diameter), 1.0/size)

cdef double pixel_luminance(double[:] rgb_pixel):
    if rgb_pixel.shape[0] == 1:
        return rgb_pixel[0]
    else:
        return 0.2989 * rgb_pixel[0] + 0.5870* rgb_pixel[1] + 0.1140 * rgb_pixel[2]

cdef double pixel_intensity(double[:] rgb_pixel):
    if rgb_pixel.shape[0] == 1:
        return rgb_pixel[0]
    else:
        return (rgb_pixel[0] + rgb_pixel[1] + rgb_pixel[2]) / 3

def convert_grayscale(double[:,:,::1] tex_2d):
    cdef Py_ssize_t tex_x_len = tex_2d.shape[0]
    cdef Py_ssize_t tex_y_len = tex_2d.shape[1]

    result = np.zeros((tex_x_len, tex_y_len, 1))
    cdef double[:,:,:] result_view = result

    for x in range(tex_x_len):
        for y in range(tex_y_len):
            result_view[x, y, 0] = pixel_luminance(tex_2d[x, y, :])

    return result

cdef pixel_hit_and_miss(long[:,:,::1] binary_tex_2d, Py_ssize_t tex_x_len, Py_ssize_t tex_y_len,
                        Py_ssize_t x, Py_ssize_t y,
                        long[:,:] struct_elem, Py_ssize_t se_i_radius, Py_ssize_t se_j_radius):
    
    cdef Py_ssize_t i, j
    cdef long current_ij

    for i in range(-se_i_radius, se_i_radius+1):
        for j in range(-se_j_radius, se_j_radius+1):
            current_ij = struct_elem[se_i_radius+i, se_j_radius+j]
            if current_ij != -1:
                if x + i >= 0 and x + i < tex_x_len and y + j >= 0 and y + j < tex_y_len:
                    if binary_tex_2d[x+i, y+j, 0] != current_ij:
                        return 0
                else:
                    return 0
    return 1


def binary_hit_and_miss(long[:,:,::1] binary_tex_2d, long[:,:] struct_elem):
    cdef Py_ssize_t tex_x_len = binary_tex_2d.shape[0]
    cdef Py_ssize_t tex_y_len = binary_tex_2d.shape[1]

    cdef Py_ssize_t se_i_radius = int((struct_elem.shape[0] - 1)/2)
    cdef Py_ssize_t se_j_radius = int((struct_elem.shape[1] - 1)/2)

    result = np.zeros((tex_x_len, tex_y_len, 1)).astype(int)
    cdef long[:,:,:] result_view = result

    cdef Py_ssize_t x, y

    for x in range(tex_x_len):
        for y in range(tex_y_len):
            result[x, y, 0] = pixel_hit_and_miss(binary_tex_2d, tex_x_len, tex_y_len, x, y,
                                                 struct_elem, se_i_radius, se_j_radius)
    return result

def binary_thinning(long[:,:,::1] binary_tex_2d):

    cdef Py_ssize_t i

    struct_elems = []
    se1 = np.array((0, 0, 0, -1, 1, -1, 1, 1, 1,)).reshape((3,3)).astype(int)
    se2 = np.array((-1, 0, 0, 1, 1, 0, -1, 1, -1,)).reshape((3,3)).astype(int)
    struct_elems.append(se1)
    struct_elems.append(se2)
    for i in range(3):
        se1 = np.rot90(se1)
        se2 = np.rot90(se2)
        struct_elems.append(se1)
        struct_elems.append(se2)

    result = np.copy(binary_tex_2d).astype(int)
    cdef long[:,:,:] result_view

    converged = False
    
    while not converged:
        new_result = np.copy(result).astype(int)
        result_view = new_result
        for i in range(8):
            new_result = new_result - binary_hit_and_miss(result_view, struct_elems[i])
            new_result = np.clip(new_result, 0, 1)
        if np.array_equal(result, new_result):
            converged = True
        result = new_result
    return result
        


def binary_erosion(long[:,:,::1] binary_tex_2d):
    cdef Py_ssize_t tex_x_len = binary_tex_2d.shape[0]
    cdef Py_ssize_t tex_y_len = binary_tex_2d.shape[1]

    cdef long[:,:] struct_elem = np.ones((3, 3)).astype(int)

    cdef Py_ssize_t se_i_radius = int((struct_elem.shape[0] - 1)/2)
    cdef Py_ssize_t se_j_radius = int((struct_elem.shape[1] - 1)/2)

    result = np.zeros((tex_x_len, tex_y_len, 1)).astype(int)
    cdef long[:,:,:] result_view = result

    cdef long acc = 0
    cdef Py_ssize_t x, y, i, j

    for x in range(tex_x_len):
        for y in range(tex_y_len):
            acc = 0
            for i in range(-se_i_radius, se_i_radius+1):
                for j in range(-se_j_radius, se_j_radius+1):
                    if x + i >= 0 and x + i < tex_x_len and y + j >= 0 and y + j < tex_y_len:
                     acc += binary_tex_2d[x+i, y+j, 0] - struct_elem[se_i_radius+i, se_j_radius+j]
            if acc == 0:
                result[x, y, 0] = 1
    return result    

def binary_dilation(long[:,:,::1] binary_tex_2d):
    cdef Py_ssize_t tex_x_len = binary_tex_2d.shape[0]
    cdef Py_ssize_t tex_y_len = binary_tex_2d.shape[1]

    cdef long[:,:] struct_elem = np.ones((3, 3)).astype(int)

    cdef Py_ssize_t se_i_radius = int((struct_elem.shape[0] - 1)/2)
    cdef Py_ssize_t se_j_radius = int((struct_elem.shape[1] - 1)/2)

    result = np.zeros((tex_x_len, tex_y_len, 1)).astype(int)
    cdef long[:,:,:] result_view = result

    cdef long acc = 0
    cdef Py_ssize_t x, y, i, j

    for x in range(tex_x_len):
        for y in range(tex_y_len):
            acc = 0
            for i in range(-se_i_radius, se_i_radius+1):
                for j in range(-se_j_radius, se_j_radius+1):
                    if x + i >= 0 and x + i < tex_x_len and y + j >= 0 and y + j < tex_y_len:
                     acc += binary_tex_2d[x+i, y+j, 0]*struct_elem[se_i_radius+i, se_j_radius+j]
            if acc > 0:
                result[x, y, 0] = 1
    return result

def onebit_posterize(double[:,:,::1] tex_2d, double threshold):
    cdef Py_ssize_t tex_x_len = tex_2d.shape[0]
    cdef Py_ssize_t tex_y_len = tex_2d.shape[1]

    result = np.zeros((tex_x_len, tex_y_len, 1))
    cdef double[:,:,:] result_view = result

    for x in range(tex_x_len):
        for y in range(tex_y_len):
            if pixel_intensity(tex_2d[x, y, :]) > threshold:
                result_view[x, y, 0] = 1.0
            else:
                result_view[x, y, 0] = 0.0

    return result.astype(int)

def convert_rgba(tex_2d, alpha):
    alphas = np.full((tex_2d.shape[0], tex_2d.shape[1], 1), alpha)
    result = np.copy(tex_2d)
    np.append(result, alphas, axis=2)
    return result

cdef clip_intensity(double[:] rgb_pixel, double max_intensity):
    cdef double intensity = pixel_intensity(rgb_pixel)
    cdef double ratio
    cdef Py_ssize_t i
    if intensity > max_intensity:
        ratio = max_intensity / intensity
        for i in range(rgb_pixel.shape[0]):
            rgb_pixel[i] = rgb_pixel[i] * ratio

@cython.boundscheck(False)
@cython.wraparound(False)
def apply_filter(double[:,:,::1] tex_2d, double[:,::1] kernel_2d,
                 double[:,:,::1] strength_mask=None, double CUTOFF=1.0):

    cdef Py_ssize_t tex_x_len = tex_2d.shape[0]
    cdef Py_ssize_t tex_y_len = tex_2d.shape[1]
    cdef Py_ssize_t tex_depth = tex_2d.shape[2]

    if strength_mask is None:
        strength_mask = np.ones((tex_x_len, tex_y_len, 1))
    assert(tex_2d.shape[0] == strength_mask.shape[0] and tex_2d.shape[1] == strength_mask.shape[1])

    cdef Py_ssize_t kern_i_radius = int((kernel_2d.shape[0] - 1)/2)
    cdef Py_ssize_t kern_j_radius = int((kernel_2d.shape[1] - 1)/2)

    result = np.zeros((tex_x_len, tex_y_len, tex_depth))
    cdef double[:,:,:] result_view = result

    cdef double[:] acc = np.zeros((tex_depth))
    cdef double intensity
    cdef Py_ssize_t x, y, i, j, k

    for x in range(tex_x_len):
        for y in range(tex_y_len):
            intensity = pixel_intensity(tex_2d[x, y, :])
            if intensity < CUTOFF:
                acc[:] = 0
                for i in range(-kern_i_radius, kern_i_radius+1):
                    for j in range(-kern_j_radius, kern_j_radius+1):
                        if x + i >= 0 and x + i < tex_x_len and y + j >= 0 and y + j < tex_y_len:
                            for k in range(len(acc)):
                                acc[k] += tex_2d[x+i, y+j, k]*kernel_2d[kern_i_radius+i, kern_j_radius+j]*strength_mask[x+i, y+j, 0]
                clip_intensity(acc, CUTOFF)
                result_view[x, y, :] = acc
            else:
                result_view[x, y, :] = tex_2d[x, y, :]
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
