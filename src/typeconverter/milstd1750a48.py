import numpy as np
from numba import njit, vectorize

signatures = [
    'f8(u8)',
]

# Reference(s):
# http://www.xgc-tek.com/manuals/mil-std-1750a/c191.html

from .twoscomp import jfunc as uint_to_twoscomp

def func(value: np.uint64) -> np.float64:
    value = np.uint64(value)
    m = np.int64(uint_to_twoscomp(
        ((value & np.uint64(0xFFFFFF000000)) >> np.uint8(8)) + (value & np.uint64(0x00000000FFFF)),
        np.uint8(40)
    ))
    e = np.int8(uint_to_twoscomp((value & np.uint64(0x000000FF0000)) >> np.uint8(16), np.uint8(8)))
    M = np.float64(m) / np.float64(2**39)
    E = np.float64(e)
    return np.float64(M * 2 ** E)

jfunc = njit(signatures)(func)
ufunc = vectorize(signatures)(func)
