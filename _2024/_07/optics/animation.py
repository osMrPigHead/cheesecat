__all__ = [
    "XZBroadcast", "MoveAlongBezier"
]

from typing import Sequence

from customs.wrappers import *
from manimlib import *


class XZBroadcast(LaggedStart):
    @ensure_type(np.ndarray, 1, "focal_point", builder=np.array)
    def __init__(
        self,
        focal_point: np.ndarray | Sequence[float],
        small_radius: float = 0.0,
        big_radius: float = 5.0,
        n_circles: int = 5,
        start_stroke_width: float = 8.0,
        color: str | Color = WHITE,
        run_time: float = 3.0,
        lag_ratio: float = 0.2,
        remover: bool = True,
        **kwargs
    ):
        self.focal_point = focal_point
        self.small_radius = small_radius
        self.big_radius = big_radius
        self.n_circles = n_circles
        self.start_stroke_width = start_stroke_width
        self.color = color

        circles = VGroup()
        for x in range(n_circles):
            circle = Circle(
                radius=big_radius,
                stroke_color=BLACK,
                stroke_width=0,
            ).rotate(PI/2, RIGHT)
            circle.add_updater(lambda c: c.move_to(focal_point))
            circle.save_state()
            circle.set_width(small_radius * 2)
            circle.set_stroke(color, start_stroke_width)
            circles.add(circle)
        super().__init__(
            *map(Restore, circles),
            run_time=run_time,
            lag_ratio=lag_ratio,
            remover=remover,
            **kwargs
        )


class MoveAlongBezier(Animation):
    def __init__(
            self,
            mobject: Mobject,
            points: Sequence[Sequence[float] | np.ndarray] | np.ndarray,
            suspend_mobject_updating: bool = False,
            **kwargs
    ):
        super().__init__(mobject, suspend_mobject_updating=suspend_mobject_updating, **kwargs)
        self.p = []
        for p in points:
            if not isinstance(p, np.ndarray):
                self.p += [np.array(p)]
                continue
            self.p += [p]
        self.n = len(self.p) - 1

    def interpolate_mobject(self, alpha: float) -> None:
        t = self.rate_func(alpha)
        self.mobject.move_to(sum((math.comb(self.n, i) * self.p[i] * (1-t)**(self.n-i) * t**i
                                  for i in range(self.n+1))))
