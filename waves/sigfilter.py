
import array


def smooth(data, N):

    output = array.array('d', data)
    for idx, val in enumerate(data):
        data_sum = 0
        for n in range(-N, N):
            if 0 <= idx + n and idx + n < len(data):
                data_sum += data[idx+n]
        output[idx] = data_sum/(2*N+1)

    return output
