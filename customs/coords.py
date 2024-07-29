"""平面解析几何
角、直线"""
__all__ = [
    "CCVector", "vectorlike", "coord",
    "CCAngle", "anglelike",
    "ZERO_ANGLE", "HALF_ANGLE", "RIGHT_ANGLE", "FLAT_ANGLE",
    "cos", "sin", "cot", "tan", "sec", "csc",
    "acos", "asin", "acot", "atan", "asec", "acsc",
    "equation_builder", "CCEquation",
]

from typing import *

import cmath

import numpy as np

from customs.wrappers import *
from manimlib import FRAME_X_RADIUS, FRAME_Y_RADIUS


# CC stands for CheeseCat
# 免得名字打架
class CCAngle:
    """复数表示的角"""
    def __init__(self, z: complex | float):
        if isinstance(z, float | int):
            z = cmath.cos(z) + 1j*cmath.sin(z)
        self._z = z

    def __pos__(self) -> Self:
        """增加 90 度 (余角为 +-Angle)"""
        return RIGHT_ANGLE + self

    def __neg__(self) -> Self:
        return CCAngle(self._z.conjugate())

    def __invert__(self) -> Self:
        """补角"""
        return FLAT_ANGLE - self

    @ensure_type(complex, 1, "other")
    def __lt__(self, other: Self | complex) -> bool:
        if self._z.imag < 0 < other.imag:
            return True
        if other.imag < 0 < self._z.imag:
            return False
        return (self._z.imag < 0 or other.imag < 0) ^ (cos(self) > cos(other))

    @ensure_type(complex, 1, "other")
    def __eq__(self, other: Self | complex) -> bool:
        return complex(self) == other

    @ensure_type(complex, 1, "other")
    def __add__(self, other: Self | complex) -> Self:
        return CCAngle(self._z * other)

    @ensure_type(complex, 1, "other")
    def __sub__(self, other: Self | complex) -> Self:
        return CCAngle(self._z * other.conjugate())

    def __mul__(self, other: float) -> Self:
        return CCAngle(self._z ** other)

    def __truediv__(self, other: float) -> Self:
        return CCAngle(self._z ** (1 / other))

    def __rshift__(self, other: Self | complex) -> bool:
        if not isinstance(other, CCAngle):
            other = CCAngle(other)
        return -RIGHT_ANGLE < self - other < RIGHT_ANGLE

    def __complex__(self) -> complex:
        return self._z


anglelike = CCAngle | complex

ZERO_ANGLE = CCAngle(1 + 0j)
HALF_ANGLE = CCAngle(1 + 1j)
RIGHT_ANGLE = CCAngle(0 + 1j)
FLAT_ANGLE = CCAngle(-1 + 0j)


@ensure_type(complex, 0, "z")
def cos(angle: anglelike) -> float:
    return angle.real / abs(angle)


def acos(x: float) -> CCAngle:
    return CCAngle(x + 1j * (1 - x ** 2) ** 0.5)


@ensure_type(complex, 0, "z")
def sin(angle: anglelike) -> float:
    return angle.imag / abs(angle)


def asin(x: float) -> CCAngle:
    return CCAngle((1 - x ** 2) ** 0.5 + 1j * x)


@ensure_type(complex, 0, "z")
def cot(angle: anglelike) -> float:
    return angle.real / angle.imag


def acot(x: float) -> CCAngle:
    return CCAngle(x + 1j)


@ensure_type(complex, 0, "z")
def tan(angle: anglelike) -> float:
    return angle.imag / angle.real


def atan(x: float) -> CCAngle:
    return CCAngle(1 + 1j * x)


@ensure_type(complex, 0, "z")
def sec(angle: anglelike) -> float:
    return abs(angle) / angle.real


def asec(x: float) -> CCAngle:
    return acos(1 / x)


@ensure_type(complex, 0, "z")
def csc(angle: anglelike) -> float:
    return abs(angle) / angle.imag


def acsc(x: float) -> CCAngle:
    return asin(1 / x)


class CCVector:
    """向量
    不用 numpy 是因为数据量不大
    还因为 PyCharm 的类型错误提示很烦人"""
    @decompose_first_tuple_m
    def __init__(self, x: float | complex | CCAngle | tuple[float, float], y: float = None):
        if isinstance(x, CCAngle):
            x = complex(x)
        if isinstance(x, complex):
            x, y = x.real, x.imag
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @ensure_type(tuple, 1, 2, "a", "b")
    def _dot(self, a: Self | tuple[float, float], b: Self | tuple[float, float]) -> float:
        return a[0] * b[0] + a[1] * b[1]

    def __abs__(self) -> float:
        return (self._x**2 + self._y**2) ** 0.5

    def __neg__(self) -> Self:
        return CCVector(-self._x, -self._y)

    def __invert__(self) -> CCAngle:
        """向量与 x 轴的夹角"""
        return CCAngle(self._x + 1j * self._y)

    @ensure_type(tuple, 1, "other")
    def __eq__(self, other: Self | tuple[float, float]) -> bool:
        return self._x == other[0] and self._y == other[1]

    @ensure_type(tuple, 1, "other")
    def __add__(self, other: Self | tuple[float, float]) -> Self:
        return CCVector(self._x + other[0], self._y + other[1])

    @ensure_type(tuple, 1, "other")
    def __sub__(self, other: Self | tuple[float, float]) -> Self:
        return CCVector(self._x - other[0], self._y - other[1])

    @overload
    def __mul__(self, other: float | int) -> Self: ...
    @overload
    def __mul__(self, other: Self | tuple[float, float]) -> float: ...

    def __mul__(self, other):
        """乘法或求内积"""
        if isinstance(other, float | int):
            return CCVector(self._x * other, self._y * other)
        return self._dot(self, other)

    @overload
    def __truediv__(self, other: float | int) -> Self: ...
    @overload
    def __truediv__(self, other: Self | tuple[float, float]) -> "CCAngle": ...

    def __truediv__(self, other):
        """除法或求夹角"""
        if isinstance(other, float | int):
            return CCVector(self.x / other, self.y / other)
        if isinstance(other, tuple):
            other = CCVector(other)
        if isinstance(other, CCVector):
            return ~self - ~other
        return NotImplemented

    def __rshift__(self, other: Self | tuple[float, float]) -> bool:
        """判断向量夹角是否为锐角 (同侧)"""
        return self * other > 0

    def __iter__(self) -> Iterator[float]:
        yield self._x
        yield self._y


vectorlike = tuple[float, float] | CCVector


def coord(x: float | vectorlike, y: float = None) -> np.ndarray:
    """ManimGL 坐标"""
    if not isinstance(x, float | int):
        x, y = x
    return np.array((x * FRAME_X_RADIUS, y * FRAME_Y_RADIUS, 0))


equation_builder = tuple[vectorlike, anglelike | float | vectorlike]


class CCEquation:
    """Ax + By = C 型直线"""
    def __init__(self, a: float, b: float, c: float):
        self._a = a
        self._b = b
        self._c = c

    @property
    def _p(self):
        if (p := self(x=0)) is not None:
            return p
        if (p := self(y=0)) is not None:
            return p

    @classmethod
    @decompose_first_tuple_m
    def build(cls, a: vectorlike | equation_builder, b: anglelike | float | vectorlike = None) \
            -> Self:
        if isinstance(b, anglelike):
            return cls.point_angle(a, b)
        if isinstance(b, float | int):
            return cls.point_oblique(a, b)
        return cls.two_points(a, b)

    @classmethod
    @ensure_type(CCVector, 1, "point")
    @ensure_type(CCAngle, 2, "angle")
    @decompose_first_tuple_m
    def point_angle(cls, point: vectorlike | tuple[vectorlike, anglelike], angle: anglelike = None) \
            -> Self:
        angle = complex(angle)
        return cls(angle.imag, -angle.real, angle.imag * point.x - angle.real * point.y)

    @classmethod
    @decompose_first_tuple_m
    def point_oblique(cls, point: vectorlike | tuple[vectorlike, float], k: float = None) \
            -> Self:
        return cls.point_angle(point, 1 + 1j*k)

    @classmethod
    @ensure_type(CCVector, 1, 2, "point1", "point2")
    @decompose_first_tuple_m
    def two_points(cls, point1: vectorlike | tuple[vectorlike, vectorlike], point2: vectorlike = None) \
            -> Self:
        return cls.point_angle(point1, ~(point2 - point1))

    def _rotate(self, point: vectorlike, angle: anglelike) -> Self:
        return self.point_angle(point, ~self + angle)

    def __call__(self, *, x: float = None, y: float = None) -> CCVector:
        """代入值"""
        if {x, y} == {None} or None not in {x, y}:
            raise TypeError()
        if x is not None:
            return self & self.point_angle((x, 0), RIGHT_ANGLE)
        return self & self.point_angle((0, y), ZERO_ANGLE)

    def __invert__(self) -> CCAngle:
        """直线与 x 轴的夹角"""
        return CCAngle(-self._b + 1j * self._a)

    def __and__(self, other: Self) -> CCVector | None:
        """联立求交点"""
        try:
            res = np.linalg.solve(np.array([[self._a, self._b], [other._a, other._b]]),
                                  np.array([self._c, other._c]))
            return CCVector(float(res[0]), float(res[1]))
        except np.linalg.LinAlgError:
            return None

    def __mul__(self, other: tuple[vectorlike, anglelike]) -> Self:
        """旋转"""
        return self._rotate(*other)

    def __truediv__(self, other: Self) -> CCAngle:
        """直线间夹角"""
        return ~self - ~other

    def __rshift__(self, other: CCVector) -> bool:
        """判断点在直线的哪一侧"""
        return CCVector(+~self) >> (other - self._p)
