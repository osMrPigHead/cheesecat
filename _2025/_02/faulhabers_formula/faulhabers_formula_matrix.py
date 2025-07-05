import math
from fractions import Fraction

import numpy as np


def expand(arr):
    return np.hstack(([[Fraction(0)] for _ in range(arr.shape[0])], arr))


if __name__ == "__main__":
    mat = np.array([[Fraction(1)]])
    for k in range(2, 12):
        mat = expand(mat)
        mat = np.vstack(((
                [math.comb(k, i) for i in range(k)] -
                [math.comb(k, i) for i in range(2, k+1)] @ mat
        ) / math.comb(k, 1), mat))
    for i in range(mat.shape[0]-1, -1, -1):
        for j in range(i, mat.shape[1]):
            print(mat[i, j], " "*(8-len(str(mat[i, j]))), sep="", end="")
        print()
