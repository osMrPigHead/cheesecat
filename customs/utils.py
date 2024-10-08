__all__ = [
    "npcross", "npforward",
    "random", "fullrand", "randbetween", "sgn",
    "included_angle", "row_nditer",
    "fade_update_", "fade_update",
    "stroke_fade_update_", "stroke_fade_update",
    "camera_update_", "camera_update",
    "color_by_z",
    "cubic_bezier", "rect_from_to"
]

import functools
from random import Random
from typing import Callable, Iterable, Sequence

from customs.wrappers import *
from manimlib import *

# PyCharm 用 np.cross 有一些奇奇怪怪的错误提示
# 就单独把 cross 函数拿出来避免这种提示 (强迫症
npcross = np.cross
random = Random(time.time())


def sgn(x: float, zero_as: int = 0) -> int:
    if x > 0:
        return 1
    if x == 0:
        return zero_as
    return -1


def fullrand(x: float | complex = 1) -> float:
    """包含正负的随机数"""
    return (random.random() * 2 - 1) * x


def randbetween(a: float | complex = -1, b: float | complex = 1) -> float:
    """生成 [a, b] 内的随机数"""
    return a + (b - a) * random.random()


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


def npforward(arr: np.ndarray, axis: int = 0) -> np.ndarray:
    return np.concatenate((arr[1:], arr[0:1]), axis)


def fade_update_(dest_opacity: float, rate_func: Callable[[float], float] = smooth, src_opacity: float = 0) \
        -> Callable[[Mobject, float], None]:
    def updater(mob: Mobject, alpha: float) -> None:
        mob.set_opacity(src_opacity + (dest_opacity - src_opacity) * rate_func(alpha))
    return updater


def fade_update(mob: Mobject, dest_opacity: float, rate_func: Callable[[float], float] = smooth,
                src_opacity: float = 0, **kwargs) \
        -> UpdateFromAlphaFunc:
    return UpdateFromAlphaFunc(mob, fade_update_(dest_opacity, rate_func, src_opacity), rate_func=linear, **kwargs)


def stroke_fade_update_(dest_opacity: float, rate_func: Callable[[float], float] = smooth, src_opacity: float = 0) \
        -> Callable[[VMobject, float], None]:
    def updater(mob: VMobject, alpha: float) -> None:
        mob.set_stroke(opacity=src_opacity + (dest_opacity - src_opacity) * rate_func(alpha))
    return updater


def stroke_fade_update(mob: VMobject, dest_opacity: float, rate_func: Callable[[float], float] = smooth,
                       src_opacity: float = 0, **kwargs) \
        -> UpdateFromAlphaFunc:
    return UpdateFromAlphaFunc(mob, stroke_fade_update_(dest_opacity, rate_func, src_opacity),
                               rate_func=linear, **kwargs)


def camera_update_(src_state: Sequence[tuple[float, np.ndarray]],
                   dst_state: Sequence[float | tuple[float, np.ndarray] |
                                       tuple[float, np.ndarray, Callable[[float], float]]],
                   dst_scale: float = 1, src_scale: float = 1, rate_func: Callable[[float], float] = smooth) \
        -> Callable[[CameraFrame, float], None]:
    _dst_state = []
    for state in dst_state:
        if len(state) == 2:
            _dst_state += [state + (smooth,)]
            continue
        if len(state) == 3:
            _dst_state += [state]

    def updater(mob: CameraFrame, alpha: float) -> None:
        mob.to_default_state()
        for s in src_state:
            mob.rotate(*s)
        for s in _dst_state:
            mob.rotate(s[2](alpha)*s[0], s[1])
        mob.scale((dst_scale - src_scale) * rate_func(alpha) + src_scale)
    return updater


def camera_update(self: Scene, src_state: Sequence[tuple[float, np.ndarray]],
                  dst_state: Sequence[tuple[float, np.ndarray] |
                                      tuple[float, np.ndarray, Callable[[float], float]]],
                  dst_scale: float = 1, src_scale: float = 1, rate_func: Callable[[float], float] = smooth, **kwargs) \
        -> UpdateFromAlphaFunc:
    return UpdateFromAlphaFunc(self.camera.frame, camera_update_(src_state, dst_state, dst_scale, src_scale, rate_func),
                               rate_func=linear, **kwargs)


def color_by_z(reference_colors: Iterable[str | Color],
               min_z: float, max_z: float,
               num: int = 32) -> Callable[[np.ndarray], np.ndarray]:
    gradient = color_gradient(
        reference_colors, num
    )
    return lambda p: (gradient[int((clip(p[2], min_z, max_z) - min_z) * num / (max_z - min_z + 1))]
                      .get_rgb())


@functools.wraps(CubicBezier)
@ensure_type(np.ndarray, 0, 1, 2, 3, "p0", "p1", "p2", "p3", builder=np.array)
def cubic_bezier(p0, p1, p2, p3, **kwargs):
    return CubicBezier(p0, p1, p2, p3, **kwargs)


@functools.wraps(Rectangle)
def rect_from_to(a: tuple[float, float], b: tuple[float, float], **kwargs) -> Rectangle:
    # 2D only
    a, b = np.array((*a, 0)), np.array((*b, 0))
    o = (a + b) / 2
    d = abs(a - b)
    return Rectangle(d[0], d[1], **kwargs).move_to(o)
