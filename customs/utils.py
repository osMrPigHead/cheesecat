__all__ = [
    "cross", "random", "fullrand", "included_angle", "row_nditer"
]

from random import Random
import time

import numpy as np

# PyCharm 用 np.cross 有一些奇奇怪怪的错误提示
# 就单独把 cross 函数拿出来避免这种提示 (强迫症
cross = np.cross
random = Random(time.time())


def fullrand(x: float | complex = 1) -> float:
    """包含正负的随机数"""
    return (random.random() * 2 - 1) * x


def included_angle(v1: np.ndarray, v2: np.ndarray) -> float:
    """向量夹角"""
    return np.arccos((v1 @ v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


def row_nditer(*op: np.ndarray, rw: bool = False):
    """生成遍历 axis=1 的 nditer"""
    op = list(op)
    for i in range(len(op)):
        op[i] = op[i].T.copy("C")
    if rw:
        return np.nditer(op, flags=["external_loop"], op_flags=[["readwrite"]], order="F")
    return np.nditer(op, flags=["external_loop"], order="F")
