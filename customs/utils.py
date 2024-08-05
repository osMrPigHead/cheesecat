__all__ = [
    "npcross", "random", "fullrand", "included_angle", "row_nditer",
    "fadein_update_", "fadein_update",
    "stroke_fadein_update_", "stroke_fadein_update",
    "camera_update_", "camera_update",
    "color_by_z"
]

from random import Random
from typing import Callable, Iterable, Sequence

from manimlib import *

# PyCharm 用 np.cross 有一些奇奇怪怪的错误提示
# 就单独把 cross 函数拿出来避免这种提示 (强迫症
npcross = np.cross
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


def fadein_update_(dest_opacity: float, rate_func: Callable[[float], float] = smooth) \
        -> Callable[[Mobject, float], None]:
    def updater(mob: Mobject, alpha: float) -> None:
        mob.set_opacity(dest_opacity * rate_func(alpha))
    return updater


def fadein_update(mob: Mobject, dest_opacity: float, rate_func: Callable[[float], float] = smooth, **kwargs) \
        -> UpdateFromAlphaFunc:
    return UpdateFromAlphaFunc(mob, fadein_update_(dest_opacity, rate_func), rate_func=linear, **kwargs)


def stroke_fadein_update_(dest_opacity: float, rate_func: Callable[[float], float] = smooth) \
        -> Callable[[VMobject, float], None]:
    def updater(mob: VMobject, alpha: float) -> None:
        mob.set_stroke(opacity=dest_opacity * rate_func(alpha))
    return updater


def stroke_fadein_update(mob: VMobject, dest_opacity: float, rate_func: Callable[[float], float] = smooth, **kwargs) \
        -> UpdateFromAlphaFunc:
    return UpdateFromAlphaFunc(mob, stroke_fadein_update_(dest_opacity, rate_func), rate_func=linear, **kwargs)


def camera_update_(src_state: Sequence[tuple[float, np.ndarray]],
                   dst_state: Sequence[float | tuple[float, np.ndarray] |
                                       tuple[float, np.ndarray, Callable[[float], float]]],
                   scale: float = 1, rate_func: Callable[[float], float] = smooth) \
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
        mob.scale((scale - 1) * rate_func(alpha) + 1)
    return updater


def camera_update(self: Scene, src_state: Sequence[tuple[float, np.ndarray]],
                  dst_state: Sequence[tuple[float, np.ndarray] |
                                      tuple[float, np.ndarray, Callable[[float], float]]],
                  scale: float = 1, rate_func: Callable[[float], float] = smooth, **kwargs) \
        -> UpdateFromAlphaFunc:
    return UpdateFromAlphaFunc(self.camera.frame, camera_update_(src_state, dst_state, scale, rate_func),
                               rate_func=linear, **kwargs)


def color_by_z(reference_colors: Iterable[str | Color],
               min_z: float, max_z: float,
               num: int = 32) -> Callable[[np.ndarray], np.ndarray]:
    return lambda p: color_gradient(
        reference_colors, num
    )[int((clip(p[2], min_z, max_z) - min_z) * num / (max_z - min_z + 1))].get_rgb()
