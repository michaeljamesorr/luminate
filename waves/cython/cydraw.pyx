#cython: language_level=3

def plot_line(double[:,:,::1] tex_2d, long x0, long y0, long x1, long y1, double[:] colour):
    assert(tex_2d.shape[2] == colour.shape[0])
    assert(x0 >= 0 and y0 >= 0 and x1 >= 0 and y1 >= 0)
    assert(x0 < tex_2d.shape[1] and y0 < tex_2d.shape[0] and x1 < tex_2d.shape[1] and y1 < tex_2d.shape[0])
    if abs(y1 - y0) < abs(x1 - x0):
        if x0 > x1:
            plot_line_low(tex_2d, x1, y1, x0, y0, colour)
        else:
            plot_line_low(tex_2d, x0, y0, x1, y1, colour)
    else:
        if y0 > y1:
            plot_line_high(tex_2d, x1, y1, x0, y0, colour)
        else:
            plot_line_high(tex_2d, x0, y0, x1, y1, colour)

cdef plot_line_low(double[:,:,::1] tex_2d, long x0, long y0, long x1, long y1, double[:] colour):
    cdef long dx = x1 - x0
    cdef long dy = y1 - y0
    cdef Py_ssize_t yi = 1
    if dy < 0:
        yi = -1
        dy = -dy
    cdef long D = 2*dy - dx
    
    cdef Py_ssize_t x, y, i
    y = y0    

    for x in range(x0, x1+1):
        for i in range(colour.shape[0]):
            tex_2d[y, x, i] = colour[i]
        if D > 0:
            y = y + yi
            D = D - 2*dx
        D = D + 2*dy


cdef plot_line_high(double[:,:,::1] tex_2d, long x0, long y0, long x1, long y1, double[:] colour):
    cdef long dx = x1 - x0
    cdef long dy = y1 - y0
    cdef Py_ssize_t xi = 1
    if dx < 0:
        xi = -1
        dx = -dx
    cdef long D = 2*dx - dy
    
    cdef Py_ssize_t x, y, i
    x = x0    

    for y in range(y0, y1+1):
        for i in range(colour.shape[0]):
            tex_2d[y, x, i] = colour[i]
        if D > 0:
            x = x + xi
            D = D - 2*dy
        D = D + 2*dx