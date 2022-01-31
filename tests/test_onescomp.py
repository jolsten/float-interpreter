import pytest
import numpy as np
from numba import njit, vectorize
from itertools import zip_longest

from typeconverter.utils import bits_to_wordsize
from typeconverter.onescomp import func, jfunc, ufunc

TEST_ARRAY_SIZE = 100
TEST_CASES = {
    3: [
        (0b000,  0),
        (0b001,  1),
        (0b010,  2),
        (0b011,  3),
        (0b100, -3),
        (0b101, -2),
        (0b110, -1),
        (0b111, -0),
    ],
    8: [
        (0b00000000,    0),
        (0b00000001,    1),
        (0b00000010,    2),
        (0b01111110,  126),
        (0b01111111,  127),
        (0b10000000, -127),
        (0b10000001, -126),
        (0b10000010, -125),
        (0b11111110,   -1),
        (0b11111111,   -0),
    ],
    16: [
        (0x0000,  0),
        (0xFFFF,  0),
    ],
    24: [
        (0x000000,  0),
        (0xFFFFFF,  0),
    ],
    32: [
        (0x00000000,  0),
        (0xFFFFFFFF,  0),
    ],
    48: [
        (0x000000000000,  0),
        (0xFFFFFFFFFFFF,  0),
    ],
    64: [
        (0x0000000000000000,  0),
        (0xFFFFFFFFFFFFFFFF,  0),
    ],
}

tests = []
for size in TEST_CASES:
    for val_in, val_out in TEST_CASES[size]:
        tests.append( (size, val_in, val_out) )


@pytest.mark.parametrize('size, val_in, val_out', tests)
def test_func(size, val_in, val_out):
    print('zzz', val_in, size, val_out)
    size = np.uint8(size)
    assert func(val_in, size) == val_out


@pytest.mark.parametrize('size, val_in, val_out', tests)
def test_njit(size, val_in, val_out):
    size = np.uint8(size)
    for bits, dtype in {8: np.uint8, 16: np.uint16, 32: np.uint32, 64: np.uint64}.items():
        if size <= bits:
            break
    val_in = dtype(val_in)
    print(val_in, val_in.dtype, size, size.dtype)
    assert jfunc(val_in, size) == val_out


@pytest.mark.parametrize('size, val_in, val_out', tests)
def test_vectorize(size, val_in, val_out):
    size = np.uint8(size)
    data = np.array([val_in] * TEST_ARRAY_SIZE, dtype=f'uint{bits_to_wordsize(size)}')
    assert all([a==b for a, b in zip_longest(ufunc(data, size), [val_out] * TEST_ARRAY_SIZE)])
