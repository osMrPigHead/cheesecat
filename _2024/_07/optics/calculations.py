"""一些计算
别问我结果怎么来的 问就是 Mathematica 帮我算的"""
__all__ = [
    "bar_magnet_b"
]

import cmath


def bar_magnet_b(i: float, wz: float, wy: float, wx: float,
                 x_: float, y_: float) -> tuple[float, float]:
    """方块的条形磁铁周围磁场分布"""
    y_ -= wy/2
    wz /= 2

    def fbx(x: float, y: float) -> float:
        return (i*(cmath.atan((x**2+y**2-x*(wz**2+x**2+y**2)**0.5)/(wz*y)) -
                   cmath.atan((wy**2+x**2+2*wy*y+y**2-x*(wz**2+wy**2+x**2+2*wy*y+y**2)**0.5) /
                              (wz*wy+wz*y)))/(2*cmath.pi)).real

    def fby(x: float, y: float) -> float:
        return (i*(2*cmath.atanh((wy**2+wz**2+x**2+2*wy*y+y**2)**0.5/wz) +
                   cmath.log(wz*(-wz+(wz**2+x**2+y**2)**0.5)) -
                   cmath.log(wz+(wz**2+x**2+y**2)**0.5))/(4*cmath.pi)).real

    try:
        return fbx(x_+wx/2, y_) - fbx(x_-wx/2, y_), fby(x_+wx/2, y_) - fby(x_-wx/2, y_)
    except ValueError:
        return 0, 0
