
import array
import numpy as np

GAUSS_BLUR_3 = np.array((1, 2, 1, 2, 4, 2, 1, 2, 1)).reshape((3, 3))/16
EDGE_DETECT = np.array((-1, -1, -1, -1, 8, -1, -1, -1, -1)).reshape((3, 3))


def average_kernel(radius):
    diameter = 2 * radius + 1
    size = diameter ** 2

    return np.full((diameter, diameter), 1.0/size)


def apply_filter(data_2d, kernel_2d):
    data_shape = data_2d.shape
    kernel_shape = kernel_2d.shape
    kernel_radius = (int((kernel_shape[0]-1)/2), int((kernel_shape[1]-1)/2))
    kernel_mid_i = kernel_radius[0]
    kernel_mid_j = kernel_radius[1]

    new_array = np.zeros(data_shape)

    for x in range(data_shape[0]):
        for y in range(data_shape[1]):
            acc = np.zeros((3))
            for i in range(-kernel_radius[0], kernel_radius[0]+1):
                for j in range(-kernel_radius[1], kernel_radius[1]+1):
                    if x + i >= 0 and x + i < data_shape[0] and y + j >= 0 and y + j < data_shape[1]:
                        acc += data_2d[x+i, y+j, :]*kernel_2d[kernel_mid_i+i, kernel_mid_j+j]
            new_array[x, y, :] = acc

    return new_array


def smooth(data, N):

    output = array.array('d', data)
    for idx, val in enumerate(data):
        data_sum = 0
        for n in range(-N, N):
            if 0 <= idx + n and idx + n < len(data):
                data_sum += data[idx+n]
        output[idx] = data_sum/(2*N+1)

    return output
