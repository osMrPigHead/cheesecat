"""立体解析几何
相当一部分内容有问题
已弃用"""
__all__ = [
    # shortcuts
    "npcross", "norm",
    # types
    "anglelike", "arraylike", "complexlike", "floatlike", "pair",
    "AngleType", "PlaneType", "LineType",
    # vector builders
    "vect3", "fullrand", "vect3rand", "coord",
    # vectorlike consts
    "ZERO_VECT", "SIGNAL", "I_VECT", "J_VECT", "K_VECT",
    "IJ_BASE2", "IK_BASE2", "JK_BASE2",
    "BREAK",
    # vector toolfuncs
    "dot_each", "projection", "base2z", "base2to3", "real",
    # trigonometry
    "cos", "c_acos", "acos", "sin", "c_asin", "asin",
    "tan", "c_atan", "atan", "cot", "c_acot", "acot",
    "sec", "c_asec", "asec", "csc", "c_acsc", "acsc",
    "c_angle_between", "angle_between", "same_side", "angle",
    # geometry builders
    "p_plane", "plane",
    "p_line", "line", "p_points2line", "points2line",
    # geometric consts
    "XY_PLANE", "XZ_PLANE", "YZ_PLANE",
    # geometric transformations
    "rotate2", "direction", "p_intersect", "intersect",
]

from abc import ABC, abstractmethod
from types import NoneType
from typing import Callable, Generic, Self, TypeVar, overload

import numpy as np

from customs.utils import *
from customs.wrappers import *
from manimlib import FRAME_X_RADIUS, FRAME_Y_RADIUS

# PyCharm 用 np.cross 有一些奇奇怪怪的错误提示
# 就单独把 cross 函数拿出来避免这种提示 (强迫症
cross = np.cross
# 单纯觉得每次打 norm 那么一长串很麻烦就单独设一个
norm = np.linalg.norm

arraylike = tuple | list | np.ndarray
boollike = bool | np.ndarray
complexlike = complex | np.ndarray
floatlike = float | np.float64 | np.ndarray
pair = tuple[np.ndarray, np.ndarray]


class _Object(ABC):
    @property
    @abstractmethod
    def data(self): ...

    @property
    @abstractmethod
    def _nditer(self) -> np.nditer: ...

    def __iter__(self) -> "_Iterator[Self]":
        return _Iterator(type(self), self._nditer)


T = TypeVar("T", bound=_Object)


class _Iterator(Generic[T]):
    def __init__(self, builder: Callable[..., T], nditer: np.nditer):
        self._builder = builder
        self._nditer = nditer

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> T:
        return self._builder(*next(self._nditer))


def vect3(x: float, y: float, z: float = 0) -> np.ndarray:
    """空间向量"""
    return np.array([x, y, z], dtype=np.float64)


ZERO_VECT = vect3(0, 0, 0)
SIGNAL = vect3(1, 1, 1)
I_VECT = vect3(1, 0, 0)
J_VECT = vect3(0, 1, 0)
K_VECT = vect3(0, 0, 1)

IJ_BASE2 = np.stack((I_VECT, J_VECT))
IK_BASE2 = np.stack((I_VECT, K_VECT))
JK_BASE2 = np.stack((J_VECT, K_VECT))

BREAK = np.stack((I_VECT + J_VECT, I_VECT + K_VECT, J_VECT + K_VECT))


def vect3rand(x: float = None, y: float = None, z: float = None) -> np.ndarray:
    return vect3(fullrand() if x is None else x,
                 fullrand() if y is None else y,
                 fullrand() if z is None else z)


@ensure_ndarray(0, 1, "a", "b")
def dot_each(a: arraylike, b: arraylike, keepdims: bool = False) -> np.ndarray:
    """逐个内积"""
    return np.sum(a * b, axis=-1, keepdims=keepdims)


@ensure_ndarray(0, 1, "vect", "break_to")
def projection(vect: arraylike, project_to: arraylike = BREAK) -> np.ndarray:
    """求空间向量在某方向上的投影"""
    return np.expand_dims(vect, axis=-2) * project_to


@ensure_ndarray(0, "base2")
def base2z(base2: arraylike) -> np.ndarray:
    """求平面基底 base2 的叉乘"""
    if not isinstance(base2, np.ndarray):
        base2 = np.stack(base2)
    return npcross(base2[..., 0, :], base2[..., 1, :])


@ensure_ndarray(0, "base2")
def base2to3(base2: arraylike) -> pair:
    """平面基底转空间基底"""
    if not isinstance(base2, np.ndarray):
        base2 = np.stack(base2)
    return np.concatenate((base2, c := np.expand_dims(base2z(base2), axis=-2)), axis=-2), c


@ensure_ndarray(0, "relative_coords")
def real(relative_coords: arraylike) -> np.ndarray:
    """相对坐标转 ManimGL 坐标"""
    assert relative_coords.shape[-1] == 3
    return relative_coords * [FRAME_X_RADIUS, FRAME_Y_RADIUS, (FRAME_X_RADIUS * FRAME_Y_RADIUS) ** 0.5]


def coord(x: float, y: float, z: float = 0) -> np.ndarray:
    """获取 ManimGL 坐标"""
    return real(vect3(x, y, z))


# 这种写法给我一种很 Java 的感觉
# 主要是为了防止自己脑子抽了把 _Angle, _Plane 或者 _Line 实例化了
class AngleType(_Object, ABC):
    """复数表示的角"""
    @abstractmethod
    def __pos__(self) -> Self:
        """增加 90 度 余角为 +-CCAngle"""
        ...

    @abstractmethod
    def __neg__(self) -> Self:
        """负角"""
        ...

    @abstractmethod
    def __invert__(self) -> Self:
        """补角"""
        ...

    @abstractmethod
    def __abs__(self) -> Self:
        """表示为锐角"""
        ...

    @abstractmethod
    def __add__(self, other: Self) -> Self:
        """求角之和"""
        ...

    @abstractmethod
    def __sub__(self, other: Self) -> Self:
        """求角之差"""
        ...

    @abstractmethod
    def __mul__(self, other: floatlike) -> Self:
        """角的乘法"""
        ...

    @abstractmethod
    def __truediv__(self, other: floatlike) -> Self:
        """角的除法"""
        ...

    @abstractmethod
    def __lshift__(self, other: arraylike) -> np.ndarray:
        """将角转换为平面上的向量"""
        ...


class _Angle(AngleType):
    def __init__(self, data: complexlike):
        self._data: complexlike = data

    @property
    def data(self) -> complexlike:
        return self._data

    @property
    def _nditer(self) -> np.nditer:
        return np.nditer(self.data, order="C")

    def __pos__(self) -> Self:
        return _Angle(1j * self._data)

    def __neg__(self) -> Self:
        return _Angle(np.conjugate(self._data))

    def __invert__(self) -> Self:
        return _Angle(-np.conjugate(self._data))

    def __abs__(self) -> Self:
        res = self
        if res._data.imag < 0:
            res = -res
        if res._data.real < 0:
            return ~res
        return res

    def __add__(self, other: Self) -> Self:
        return _Angle(self._data * other._data)

    def __sub__(self, other: Self) -> Self:
        return _Angle(self._data * (-other)._data)

    def __mul__(self, other: floatlike) -> Self:
        return _Angle(self._data ** other)

    def __truediv__(self, other: floatlike) -> Self:
        return _Angle(self._data ** (1 / other))

    @ensure_ndarray(1, "other")
    def __lshift__(self, other: arraylike) -> np.ndarray:
        return other[..., 0, :] * np.real(self._data) + other[..., 1, :] * np.imag(self._data)


anglelike = complex | float | AngleType


def cos(a: complexlike | _Angle, b: np.ndarray = None) -> floatlike:
    """两向量夹角余弦或角的余弦"""
    if b is None:
        np.real(a.data if isinstance(a, _Angle) else a)
    return dot_each(a, b) / dot_each(norm(a, axis=-1, keepdims=True),
                                     norm(b, axis=-1, keepdims=True))


def c_acos(x: floatlike) -> complexlike:
    """反余弦函数 (返回复数)"""
    return x + 1j*(1 - x**2) ** 0.5


def acos(x: floatlike) -> _Angle:
    """反余弦函数 (返回对象)"""
    return _Angle(c_acos(x))


def sin(a: complexlike | _Angle, b: np.ndarray = None) -> floatlike:
    """两向量夹角正弦或角的正弦"""
    if b is None:
        np.imag(a.data if isinstance(a, _Angle) else a)
    return (1 - cos(a, b)**2) ** 0.5


def c_asin(x: floatlike) -> complexlike:
    """反正弦函数 (返回复数)"""
    return (1 - x**2) ** 0.5 + 1j*x


def asin(x: floatlike) -> _Angle:
    """反正弦函数 (返回对象)"""
    return _Angle(c_asin(x))


def tan(a: complexlike | _Angle, b: np.ndarray = None) -> floatlike:
    """两向量夹角正切或角的正切"""
    return sin(a, b) / cos(a, b)


def c_atan(x: floatlike) -> complexlike:
    """反正切函数 (返回复数)"""
    return 1 + 1j*x


def atan(x: floatlike) -> _Angle:
    """反正切函数 (返回对象)"""
    return _Angle(c_atan(x))


def cot(a: complexlike | _Angle, b: np.ndarray = None) -> floatlike:
    """两向量夹角余切或角的余切"""
    return cos(a, b) / sin(a, b)


def c_acot(x: floatlike) -> complexlike:
    """反正切函数 (返回复数)"""
    return x + 1j


def acot(x: floatlike) -> _Angle:
    """反正切函数 (返回对象)"""
    return _Angle(c_acot(x))


def sec(a: complexlike | _Angle, b: np.ndarray = None) -> floatlike:
    """两向量夹角正割或角的正割"""
    return 1 / cos(a, b)


def c_asec(x: floatlike) -> complexlike:
    """反正割函数 (返回复数)"""
    return c_acos(1 / x)


def asec(x: floatlike) -> _Angle:
    """反正割函数 (返回复数)"""
    return _Angle(c_asec(x))


def csc(a: complexlike | _Angle, b: np.ndarray = None) -> floatlike:
    """两向量夹角余割或角的余割"""
    return 1 / sin(a, b)


def c_acsc(x: floatlike) -> complexlike:
    """反余割函数 (返回复数)"""
    return c_asin(1 / x)


def acsc(x: floatlike) -> _Angle:
    """反余割函数 (返回复数)"""
    return _Angle(c_acsc(x))


def c_angle_between(a: np.ndarray, b: np.ndarray) -> complexlike:
    """两向量夹角的复数表示 (返回复数)"""
    return cos(a, b) + sin(a, b) * 1j


def angle_between(a: np.ndarray, b: np.ndarray) -> _Angle:
    """两向量夹角的复数表示 (返回对象)"""
    return _Angle(c_angle_between(a, b))


def same_side(a: np.ndarray, b: np.ndarray) -> boollike:
    """判断两向量是否同侧 (夹角为锐角)"""
    return cos(a, b) > 0


def angle(z: complexlike) -> _Angle:
    return _Angle(z)


class _Equation(_Object, ABC):
    def __init__(self, builder: Callable[[np.ndarray, np.ndarray], Self],
                 different: list[type["_Equation"]]):
        self._builder = builder
        self._different = different

    @property
    def _nditer(self) -> np.nditer:
        return row_nditer(*self.data)

    @property
    @abstractmethod
    def reference(self) -> np.ndarray:
        """选取参考点"""
        ...

    def __call__(self, x: floatlike = None, y: floatlike = None, z: floatlike = None) \
            -> floatlike:
        """代入数值"""
        if not isinstance(x, np.ndarray) and x is not None:
            x = np.array([x], dtype=np.float64)
        if not isinstance(y, np.ndarray) and y is not None:
            y = np.array([y], dtype=np.float64)
        if not isinstance(z, np.ndarray) and z is not None:
            z = np.array([z], dtype=np.float64)
        if None not in (s := {x, y, z}) or s == {None}:
            raise ValueError()
        res = self
        if x is not None:
            res = intersect(res, (np.tile(I_VECT, x.shape), x))
        if y is not None and res is not None:
            res = intersect(res, (np.tile(J_VECT, y.shape), y))
        if z is not None and res is not None:
            res = intersect(res, (np.tile(K_VECT, z.shape), z))
        return res

    def __mul__(self, other: anglelike |
                             tuple[anglelike] |
                             tuple[anglelike, np.ndarray] |
                             tuple[np.ndarray, anglelike | np.ndarray, np.ndarray] |
                             tuple[np.ndarray, anglelike]) \
            -> Self:
        """旋转
        angle
        (angle)
        (angle, p)
        (base2, angle, p)
        (base2, angle)"""
        p = vect = None
        if not isinstance(other, tuple):
            other = (other,)
        if len(other) == 1:
            p = rotate2(other[0], self.reference)
            vect = rotate2(other[0], direction(self))
        if len(other) == 2:
            if isinstance(other[0], np.ndarray):
                p = rotate2(*other, self.reference)
                vect = rotate2(*other, direction(self))
            else:
                p = rotate2(other[0], self.reference, other[1])
                vect = rotate2(other[0], direction(self))
        if len(other) == 3:
            p = rotate2(other[0], other[1], self.reference, other[2])
            vect = rotate2(other[0], other[1], direction(self))
        return self._builder(p, vect)

    @ensure_ndarray(1, "other")
    @abstractmethod
    def __rshift__(self, other: arraylike) -> bool:
        """判断同侧"""
        ...


@ensure_ndarray(0, 1, "point", "normal")
def p_plane(point: arraylike, normal: arraylike) -> pair:
    """平面 (返回 pair)"""
    if len(normal.shape) == 1 or normal.shape[-2] != 1:
        normal = np.expand_dims(normal, axis=-2)
    return normal, dot_each(normal, point)


@ensure_ndarray(0, 1, "point", "normal")
def plane(point: arraylike, normal: arraylike) -> "_Plane":
    """平面 (返回对象)"""
    return _Plane(*p_plane(point, normal))


class PlaneType(_Equation, ABC):
    """平面"""
    @property
    @abstractmethod
    def base2(self):
        """获取平面上的一组正交基底"""
        return

    @abstractmethod
    def __and__(self, other: _Equation) -> np.ndarray | _Equation | NoneType:
        """求交点或交线"""
        ...

    @abstractmethod
    def __truediv__(self, other: _Equation | np.ndarray) -> _Angle:
        """求夹角 (有向)"""
        ...

    @abstractmethod
    def __floordiv__(self, other: _Equation) -> _Angle:
        """求夹角 (无向)"""
        ...

    @abstractmethod
    def __lshift__(self, other: arraylike) -> np.ndarray:
        """向量在平面上的投影"""
        ...

    @abstractmethod
    def __rshift__(self, other: arraylike) -> boollike:
        """判断同侧"""
        ...


class _Plane(PlaneType):
    def __init__(self, normal: np.ndarray, d: np.ndarray):
        super().__init__(plane, [_Line])
        self.normal = normal
        self.d = d
    
    @property
    def data(self) -> pair:
        return self.normal, self.d

    @property
    def reference(self) -> np.ndarray:
        if (res := self(x=0, y=0)) is not None:
            return res
        if (res := self(x=0, z=0)) is not None:
            return res
        if (res := self(y=0, z=0)) is not None:
            return res

    @property
    def base2(self) -> np.ndarray:
        d = 1
        if (res := (self(x=0, y=0), self(x=d, y=0), self(x=0, y=d))) is not None:
            return np.stack([res[1] - res[0], res[2] - res[0]], axis=-2)
        if (res := (self(x=0, z=0), self(x=d, z=0), self(x=0, z=d))) is not None:
            return np.stack([res[1] - res[0], res[2] - res[0]], axis=-2)
        if (res := (self(y=0, z=0), self(y=d, z=0), self(y=0, z=d))) is not None:
            return np.stack([res[1] - res[0], res[2] - res[0]], axis=-2)
    
    def __and__(self, other: _Equation) -> np.ndarray | _Equation | NoneType:
        return intersect(self, other)

    def __truediv__(self, other: _Equation | np.ndarray) -> _Angle:
        if isinstance(other, np.ndarray):
            return +-angle_between(direction(self), other)
        if isinstance(other, _Line):
            return +-angle_between(direction(self), direction(other))
        return angle_between(direction(self), direction(other))

    def __floordiv__(self, other: _Equation) -> _Angle:
        return abs(self / other)

    @ensure_ndarray(1, "other")
    def __lshift__(self, other: arraylike) -> np.ndarray:
        return projection(other, base2 := self.base2) @ base2 + self.reference

    @ensure_ndarray(1, "other")
    def __rshift__(self, other: arraylike) -> boollike:
        return same_side(self.normal, other - self.reference)


@overload
def p_line(point: np.ndarray, direction: np.ndarray) -> pair: ...
@overload
def p_line(base2: arraylike, point: np.ndarray, direction: np.ndarray) -> pair: ...
@overload
def p_line(base2: arraylike, point: np.ndarray, k: float) -> pair: ...
@overload
def p_line(point: np.ndarray, k: float) -> pair: ...


def p_line(a, b, c=None):
    """直线 参数式 点斜式 (返回 pair)"""
    if c is not None:
        if isinstance(c, float):
            c = np.array([1, c], dtype=np.float64)
        if not isinstance(c, np.ndarray):
            c = np.stack(c)
        a, b = b, c @ a
    if isinstance(b, float):
        b = np.array([1, b], dtype=np.float64) @ IJ_BASE2
    if not isinstance(b, np.ndarray):
        b = np.stack(b)
    x = np.concatenate((npcross(bb := projection(b), [1, 1, 1]) * BREAK,
                        dot_each(npcross(bb, projection(a)), SIGNAL, keepdims=True)), axis=-1)
    x = x[..., 0, :] + x[..., 1, :] * (
            (np.sum(x[..., 0, 0:3], axis=-1, keepdims=True) == 0) |
            (np.sum(((s := np.sum(x, axis=-2)) - x)[..., 0, 0:3], axis=-1, keepdims=True) == 0)
    )
    return (res := np.stack((s, s - x), axis=-2))[..., 0:3], res[..., 3]


@overload
def line(point: np.ndarray, direction: np.ndarray) -> "_Line": ...
@overload
def line(base2: arraylike, point: np.ndarray, direction: np.ndarray) -> "_Line": ...
@overload
def line(base2: arraylike, point: np.ndarray, k: float) -> "_Line": ...
@overload
def line(point: np.ndarray, k: float) -> "_Line": ...


def line(a, b, c=None):
    """直线 参数式 点斜式 (返回对象)"""
    return _Line(*p_line(a, b, c))


@ensure_ndarray(0, 1, "p1", "p2")
def p_points2line(p1: arraylike, p2: arraylike) -> pair:
    """直线 两点式 (返回 pair)"""
    return p_line(p1, p2 - p1)


@ensure_ndarray(0, 1, "p1", "p2")
def points2line(p1: arraylike, p2: arraylike) -> "_Line":
    """直线 两点式 (返回对象)"""
    return _Line(*p_points2line(p1, p2))


class LineType(_Equation, ABC):
    """直线"""
    def __invert__(self) -> _Plane:
        """求 z 轴方向的投影面"""
        ...

    @abstractmethod
    def __and__(self, other: _Equation) -> np.ndarray | _Equation | NoneType:
        """求交点"""
        ...

    @abstractmethod
    def __truediv__(self, other: _Equation | np.ndarray) -> _Angle:
        """求夹角 (有向)"""
        ...

    @abstractmethod
    def __floordiv__(self, other: _Equation) -> _Angle:
        """求夹角 (无向)"""
        ...

    @abstractmethod
    def __pow__(self, other: arraylike) -> _Plane:
        """求某方向上的投影面"""
        ...

    @abstractmethod
    def __lshift__(self, other: PlaneType) -> "_Line":
        """直线在平面上的投影"""
        ...

    @abstractmethod
    def __rshift__(self, other: arraylike) -> boollike:
        """判断同向"""
        ...


class _Line(LineType):
    def __init__(self, normals: np.ndarray, ds: np.ndarray):
        super().__init__(line, [_Plane])
        self.normals = normals
        self.ds = ds
    
    @property
    def data(self) -> pair:
        return self.normals, self.ds

    @property
    def reference(self) -> np.ndarray:
        if (res := self(x=0)) is not None:
            return res
        if (res := self(y=0)) is not None:
            return res
        if (res := self(z=0)) is not None:
            return res

    def __invert__(self) -> _Plane:
        return self ** K_VECT

    def __and__(self, other: _Equation) -> np.ndarray | NoneType:
        return intersect(self, other)

    def __truediv__(self, other: _Equation) -> _Angle:
        if isinstance(other, np.ndarray):
            return angle_between(direction(self), other)
        if isinstance(other, _Plane):
            return +-angle_between(direction(self), direction(other))
        return angle_between(direction(self), direction(other))

    def __floordiv__(self, other: _Equation) -> _Angle:
        return abs(self / other)

    def __pow__(self, other: arraylike) -> _Plane:
        return plane(self.reference, npcross(direction(self), other))

    def __lshift__(self, other: PlaneType) -> "_Line":
        return line(other << self.reference, other << direction(self))

    @ensure_ndarray(1, "other")
    def __rshift__(self, other: arraylike) -> boollike:
        return same_side(direction(self), other)


XY_PLANE = plane(ZERO_VECT, K_VECT)
XZ_PLANE = plane(ZERO_VECT, J_VECT)
YZ_PLANE = plane(ZERO_VECT, I_VECT)


@overload
def rotate2(base2: arraylike, angle: anglelike | np.ndarray, x: np.ndarray, p: np.ndarray = ...) -> np.ndarray: ...
@overload
def rotate2(angle: anglelike, x: np.ndarray, p: np.ndarray = ...) -> np.ndarray: ...


def rotate2(base2, angle, x=ZERO_VECT, p=ZERO_VECT):
    """以 base2 在 p 处的法线为轴旋转"""
    if not isinstance(base2, np.ndarray) and not isinstance(base2, tuple):
        base2, angle, x, p = IJ_BASE2, base2, angle, x
    if not isinstance(base2, np.ndarray):
        base2 = np.stack(base2)
    if isinstance(angle, _Object):
        angle = angle.data
    if not isinstance(angle, np.ndarray):
        angle = np.array([angle])
    if angle.dtype.type != np.complex128:
        angle = np.exp(1j*angle)
    angle /= abs(angle)
    if angle.shape != (1,):
        angle = np.expand_dims(angle, axis=-1)
    angle = np.stack((angle, angle, np.ones(angle.shape)), axis=-2)
    base3, c = base2to3(base2)
    base2j = ((d := npcross(c, base2)) * norm(base2, axis=-1, keepdims=True) /
              norm(d, axis=-1, keepdims=True))
    return ((x - p) @ np.concatenate((np.real(base2 * angle + base2j * 1j*angle), c), axis=-2) @
            np.linalg.inv(base3) + p)


def direction(x: pair | _Equation) -> np.ndarray:
    """求直线的方向向量或平面的法向量"""
    if isinstance(x, _Equation):
        x = x.data
    if x[0].shape[-2] == 1:
        return np.squeeze(x[0], axis=-2)
    return base2z(x[0])


def p_intersect(a: pair | _Equation, b: pair | _Equation) -> np.ndarray | pair | NoneType:
    """求直线或平面的交点或交线 (返回 pair)"""
    if isinstance(a, _Equation):
        a = a.data
    if isinstance(b, _Equation):
        b = b.data
    if a[0].shape[-2] == b[0].shape[-2] == 1:
        return np.concatenate((a[0], b[0]), axis=-2), np.concatenate((a[1], b[1]), axis=-2)
    if {a[0].shape[-2], b[0].shape[-2]} == {1, 2}:
        try:
            return np.linalg.solve(np.concatenate((a[0], b[0]), axis=-2),
                                   np.concatenate((a[1], b[1]), axis=-2))
        except np.linalg.LinAlgError:
            return None
    # KX = C
    k = np.concatenate((a[0], b[0][..., 0, :]), axis=-2)
    c = np.concatenate((a[1], b[1][..., 0, :]), axis=-2)
    try:
        np.linalg.solve(np.concatenate((k, c), axis=-1),
                        np.concatenate((b[0][..., 1, :], b[1][..., 1, :]), axis=-1))
        return np.linalg.solve(k, c)
    except np.linalg.linalg.LinAlgError:
        return None


def intersect(a: pair | _Equation, b: pair | _Equation) -> np.ndarray | _Line | NoneType:
    if isinstance(res := p_intersect(a, b), tuple):
        return _Line(*res)
    return res
