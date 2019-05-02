import numpy as np
cimport numpy as cnp
import cython

@cython.boundscheck(False)
@cython.wraparound(False)
def calculate_signals(cnp.ndarray[double, ndim=2] offsets, cnp.ndarray sig):

    cdef int signal_len     = int(sig.shape[1]/4)
    cdef int channels_count = sig.shape[0]
    cdef int offsets_count  = offsets.shape[0]

    cdef cnp.ndarray[double, ndim=2] shifted = np.empty((channels_count, signal_len), dtype=np.double)
    cdef cnp.ndarray[double, ndim=2] result  = np.empty((offsets_count, signal_len), dtype=np.double)

    cdef int i,j
    for i in range(offsets_count):
        for j in range(channels_count):
            shifted[j] = _shift(sig[j],offsets[i, j])[0::4]
        result[i] = np.sum(shifted, axis=0, dtype=np.double)
    return result

def _shift(cnp.ndarray arr, short num):
    cdef cnp.ndarray[double] result = np.empty_like(arr, dtype=np.double)
    if num > 0:
        result[:num] = 0
        result[num:] = arr[:-num]
    elif num < 0:
        result[num:] = 0
        result[:num] = arr[-num:]
    else:
        result[:] = arr
    return result

@cython.boundscheck(False)
@cython.wraparound(False)
def powers(cnp.ndarray[double] x, cnp.ndarray[double] y, cnp.ndarray[short] ki):
    cdef double e = 0
    cdef double s = 0

    cdef int k
    for k in range(*ki):
        s = np.dot(x,_shift(y,k))
        if s>e:
           e=s
    return e

@cython.boundscheck(False)
@cython.wraparound(False)
def powers_all(cnp.ndarray[double, ndim=2] sig1, cnp.ndarray[double, ndim=2] sig2):
    cdef cnp.ndarray[short, ndim=3]  km = np.array([[[-3,3+1]]*31]*31, dtype='short')
    cdef cnp.ndarray[double, ndim=2] rm = np.empty((31,31), dtype=np.double)

    cdef int res_w = km.shape[0]
    cdef int res_h = km.shape[1]

    cdef int i,j
    for i in range(res_w):
        for j in range(res_h):
            rm[i, j] = powers(sig1[i],sig2[j],km[i, j])
    return rm


def calculate(cnp.ndarray sig1, cnp.ndarray sig2, cnp.ndarray[double, ndim=2] offsets):

    result1 = calculate_signals(offsets, sig1.T)
    result2 = calculate_signals(offsets, sig2.T)

    return powers_all(result1, result2)
