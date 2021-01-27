import numpy as np
cimport numpy as cnp
import cython

# функція обрахунку сум
@cython.boundscheck(False)
@cython.wraparound(False)
def calculate_signals(cnp.ndarray[double, ndim=2] offsets, cnp.ndarray sig):
    # довжіна масиву сигналу, ділимо на 4 через те що ми зменшуємо кількість данних у 4 рази для пришвидшення обрахунків
    cdef int signal_len     = int(sig.shape[1]/4)
    # кількість каналів
    cdef int channels_count = sig.shape[0]
    # довжина масиву зміженя 31
    cdef int offsets_count  = offsets.shape[0]

    # масив зміщений пустий
    cdef cnp.ndarray[double, ndim=2] shifted = np.empty((channels_count, signal_len), dtype=np.double)
    # масиву результуючий пустий
    cdef cnp.ndarray[double, ndim=2] result  = np.empty((offsets_count, signal_len), dtype=np.double)

    cdef int i,j
    # проходимо по усіх каналах усіх зміщень
    for i in range(offsets_count):
        for j in range(channels_count):
            # робимо зміщення для сигналу с певним каналом, зменшуємо кількість даних у 4 рази
            shifted[j] = _shift(sig[j],offsets[i, j])[0::4]
        # записуємо суму у результуючий масив усі значення в зміщеному масиві
        result[i] = np.sum(shifted, axis=0, dtype=np.double)
    return result

# Функція яка зміщує сигнал на задану кількість кроків
def _shift(cnp.ndarray arr, short num):
    # створюємо новий пустий масив
    cdef cnp.ndarray[double] result = np.empty_like(arr, dtype=np.double)
    # якщо кількість додатня зміщуємо в право
    if num > 0:
        result[:num] = 0
        result[num:] = arr[:-num]
    # якщо кількість відємна то зміщуємо в ліво
    elif num < 0:
        result[num:] = 0
        result[:num] = arr[-num:]
    # інакше попертаємо вхідний масив
    else:
        result[:] = arr
    return result

# функція віконує скалярне множення усіх масивів з заданим зміженням k
@cython.boundscheck(False)
@cython.wraparound(False)
def powers(cnp.ndarray[double] x, cnp.ndarray[double] y, cnp.ndarray[short] ki):
    cdef double e = 0
    cdef double s = 0

    cdef int k
    for k in range(*ki):
        # скалаярне множення
        s = np.dot(x,_shift(y,k))
        if s>e:
           e=s
    return e

# ця функія проходе по сигналам 1 та 2 та по усім зміщенням
@cython.boundscheck(False)
@cython.wraparound(False)
def powers_all(cnp.ndarray[double, ndim=2] sig1, cnp.ndarray[double, ndim=2] sig2):
    # створення масивів
    cdef cnp.ndarray[short, ndim=3]  km = np.array([[[-3,3+1]]*31]*31, dtype='short')
    cdef cnp.ndarray[double, ndim=2] rm = np.empty((31,31), dtype=np.double)

    # розмірність матриці зміщень
    cdef int res_w = km.shape[0]
    cdef int res_h = km.shape[1]

    cdef int i,j
    for i in range(res_w):
        for j in range(res_h):
            # формування результуючої матриці та процедураскалярно множення
            rm[i, j] = powers(sig1[i],sig2[j],km[i, j])
    return rm

# функція яка обєднує усі обераціє, усі інші операції можна вважати приватними, вихідний метод модуля апі
def calculate(cnp.ndarray sig1, cnp.ndarray sig2, cnp.ndarray[double, ndim=2] offsets):

    result1 = calculate_signals(offsets, sig1.T)
    result2 = calculate_signals(offsets, sig2.T)

    return powers_all(result1, result2)
