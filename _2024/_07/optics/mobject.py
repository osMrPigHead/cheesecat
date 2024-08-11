__all__ = [
    "ElectronmagneticPair", "ElectronmagneticPairUpdater",
    "ElectronmagneticField", "ElectronmagneticFieldUpdater",
    "Ball", "Charge", "AxesCharge", "Electron",
    "BarMagnet"
]

from typing import Callable, Self, Sequence

from noise import pnoise1

from customs.constants import *
from customs.utils import *
from customs.wrappers import *
from manimlib import *


class ElectronmagneticPair(VGroup):
    @ensure_type(np.ndarray, 1, 2, 3, "coords", "e_value", "b_value", builder=np.array)
    def __init__(
            self,
            coords: np.ndarray | Sequence[float],
            e_value: np.ndarray | Sequence[float],
            b_value: np.ndarray | Sequence[float],
            coordinate_system: CoordinateSystem,
            e_color: str | Color = GREEN_E,
            b_color: str | Color = BLUE_D,
            opacity: float = 1,
            vector_config: dict = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if vector_config is None:
            vector_config = {}
        self.coords = coords
        self.e_value = e_value
        self.b_value = b_value
        self.coordinate_system = coordinate_system
        self.e_color = e_color
        self.b_color = b_color
        self.opacity = opacity
        self.vector_config = vector_config

        self._start = coordinate_system.c2p(*coords)
        self._e_vect = coordinate_system.c2p(*(coords + e_value))
        self._b_vect = coordinate_system.c2p(*(coords + b_value))

        self.e_mob = Arrow(self._start, self._e_vect,
                           stroke_color=e_color, stroke_opacity=opacity, buff=0,
                           **vector_config)
        self.b_mob = Arrow(self._start, self._b_vect,
                           stroke_color=b_color, stroke_opacity=opacity, buff=0,
                           **vector_config)
        self.add(self.e_mob, self.b_mob)

    @ensure_type(np.ndarray, 1, "coords", builder=np.array)
    def set_coords(self, coords: np.ndarray | Sequence[float]) -> Self:
        if tuple(coords) == tuple(self.coords):
            return
        self.e_mob.shift((start := self.coordinate_system.c2p(*coords)) - self._start)
        self.b_mob.shift(start - self._start)

        self.coords = coords
        self._start = start
        self._e_vect = self.coordinate_system.c2p(*(coords + self.e_value))
        self._b_vect = self.coordinate_system.c2p(*(coords + self.b_value))

        return self

    @ensure_type(np.ndarray, 1, "e_value", builder=np.array)
    def set_e_value(self, e_value: np.ndarray | Sequence[float]) -> Self:
        if tuple(e_value) == tuple(self.e_value):
            return
        self.e_value = e_value
        self._e_vect = self.coordinate_system.c2p(*(self.coords + e_value))
        self.e_mob.put_start_and_end_on(self._start, self._e_vect)

        return self

    @ensure_type(np.ndarray, 1, "e_value", builder=np.array)
    def set_b_value(self, b_value: np.ndarray | Sequence[float]) -> Self:
        if tuple(b_value) == tuple(self.b_value):
            return
        self.b_value = b_value
        self._b_vect = self.coordinate_system.c2p(*(self.coords + b_value))
        self.b_mob.put_start_and_end_on(self._start, self._b_vect)

        return self


class ElectronmagneticPairUpdater(ElectronmagneticPair):
    def __init__(
            self,
            coords: np.ndarray | Sequence[float],
            e_func_t: Callable[[float], Sequence[float] | np.ndarray],
            b_func_t: Callable[[float], Sequence[float] | np.ndarray],
            coordinate_system: CoordinateSystem,
            e_color: str | Color = GREEN_E,
            b_color: str | Color = BLUE_D,
            opacity: float = 1,
            vector_config: dict = None,
            **kwargs
    ):
        super().__init__(
            coords,
            e_func_t(0),
            b_func_t(0),
            coordinate_system,
            e_color,
            b_color,
            opacity,
            vector_config,
            **kwargs
        )
        self.time = 0
        self.e_func_t = e_func_t
        self.b_func_t = b_func_t

        self.add_updater(lambda mob, dt: mob.increase_time(dt))

    def increase_time(self, dt) -> Self:
        self.time += dt
        self.set_e_value(self.e_func_t(self.time))
        self.set_b_value(self.b_func_t(self.time))

        return self

    def set_time(self, t) -> Self:
        return self.increase_time(t - self.time)

    def set_e_func_t(self, e_func_t: Callable[[float], Callable[..., Sequence[float]]]) -> Self:
        self.e_func_t = e_func_t
        self.set_e_value(self.e_func_t(self.time))

        return self

    def set_b_func_t(self, b_func_t: Callable[[float], Callable[..., Sequence[float]]]) -> Self:
        self.b_func_t = b_func_t
        self.set_b_value(self.b_func_t(self.time))

        return self


class ElectronmagneticField(VGroup):
    def __init__(
            self,
            e_func: Callable[..., Sequence[float] | np.ndarray],
            b_func: Callable[..., Sequence[float] | np.ndarray],
            coordinate_system: CoordinateSystem,
            step_multiple: float = 0.5,
            e_color: str | Color = GREEN_E,
            b_color: str | Color = BLUE_D,
            opacity: float = 1,
            vector_config: dict = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if vector_config is None:
            vector_config = {}
        self.e_func = e_func
        self.b_func = b_func
        self.coordinate_system = coordinate_system
        self.step_multiple = step_multiple
        self.e_color = e_color
        self.b_color = b_color
        self.opacity = opacity
        self.vector_config = vector_config

        self._mobs = self.get_mobs()
        self.add(*self._mobs.values())

    def get_mobs(self) -> dict[tuple, ElectronmagneticPair]:
        mobs = {}
        for coords in get_sample_points_from_coordinate_system(
                self.coordinate_system,
                self.step_multiple
        ):
            mobs[tuple(coords)] = ElectronmagneticPair(
                coords,
                self.e_func(*coords),
                self.b_func(*coords),
                self.coordinate_system,
                self.e_color,
                self.b_color,
                self.opacity,
                self.vector_config
            )
        return mobs

    def set_e_func(self, e_func: Callable[..., Sequence[float]]) -> Self:
        for coords, mob in zip(self._mobs.keys(), self._mobs.values()):
            mob.set_e_value(e_func(*coords))

        self.e_func = e_func

        return self

    def set_b_func(self, b_func: Callable[..., Sequence[float]]) -> Self:
        for coords, mob in zip(self._mobs.keys(), self._mobs.values()):
            mob.set_b_value(b_func(*coords))

        self.e_func = b_func

        return self


class ElectronmagneticFieldUpdater(ElectronmagneticField):
    def __init__(
            self,
            e_func_t: Callable[[float], Callable[..., Sequence[float] | np.ndarray]],
            b_func_t: Callable[[float], Callable[..., Sequence[float] | np.ndarray]],
            coordinate_system: CoordinateSystem,
            step_multiple: float = 0.5,
            e_color: str | Color = GREEN_E,
            b_color: str | Color = BLUE_D,
            opacity: float = 1,
            vector_config: dict = None,
            **kwargs
    ):
        super().__init__(
            e_func_t(0),
            b_func_t(0),
            coordinate_system,
            step_multiple,
            e_color,
            b_color,
            opacity,
            vector_config,
            **kwargs
        )
        self.time = 0
        self.e_func_t = e_func_t
        self.b_func_t = b_func_t

        self.add_updater(lambda mob, dt: mob.increase_time(dt))

    def increase_time(self, dt) -> Self:
        self.time += dt
        self.set_e_func(self.e_func_t(self.time))
        self.set_b_func(self.b_func_t(self.time))

        return self

    def set_time(self, t) -> Self:
        return self.increase_time(t - self.time)

    def set_e_func_t(self, e_func_t: Callable[[float], Callable[..., Sequence[float]]]) -> Self:
        self.e_func_t = e_func_t
        self.set_e_func(self.e_func_t(self.time))

        return self

    def set_b_func_t(self, b_func_t: Callable[[float], Callable[..., Sequence[float]]]) -> Self:
        self.b_func_t = b_func_t
        self.set_b_func(self.b_func_t(self.time))

        return self


class Ball(TrueDot):
    def __init__(
            self,
            pos: tuple[float, float, float] | np.ndarray,
            radius: float = 0.3,
            three_d: bool = True,
            color: str | Color | None = GREY,
            text: str | None = None,
            font_size: int = 48,
            **kwargs
    ):
        super().__init__(radius=radius, color=color, **kwargs)
        if three_d:
            self.make_3d()
        self.add(Text([text, ""][text is None], font_size=font_size))
        self.move_to(pos)

    @property
    def pos(self) -> np.ndarray:
        return self[0].get_center()


class Charge(Ball):
    def __init__(
            self,
            pos: tuple[float, float, float] | np.ndarray,
            kq: float,
            radius: float = 0.3,
            font_size: int = 48,
            three_d: bool = True,
            **kwargs
    ):
        positive = kq > 0
        self.kq = kq

        super().__init__(pos, radius, three_d, [BLUE, RED][positive],
                         [EN_DASH, "+"][positive] if font_size else "", font_size if font_size else 48, **kwargs)

    def get_e(self, pos: tuple[float, float, float] | np.ndarray) -> np.ndarray:
        if norm := get_norm(vect := self.pos - pos):
            return self.kq / norm ** 2 * -normalize(vect)
        return np.zeros((3,))

    def get_phi(self, pos: tuple[float, float, float] | np.ndarray) -> float:
        if norm := get_norm(self.pos - pos):
            return self.kq / norm
        return np.inf


class AxesCharge(Charge):
    def __init__(
            self,
            axes: CoordinateSystem,
            coords: tuple[float, ...],
            kq: float,
            radius: float = 0.3,
            font_size: int = 48,
            three_d: bool = True,
            **kwargs
    ):
        self.axes = axes
        super().__init__(axes.c2p(*coords), kq, radius, font_size, three_d, **kwargs)

    @property
    def coords(self) -> np.ndarray:
        return np.array(self.axes.p2c(self.pos))

    def get_e(self, x: tuple[float, ...] | np.ndarray, real: bool = False) -> np.ndarray:
        if real:
            return super().get_e(x)
        if norm := get_norm(vect := self.coords - x):
            return self.kq / norm ** 2 * -normalize(vect)
        return np.zeros(self.coords.shape)

    def get_phi(self, x: tuple[float, ...] | np.ndarray, real: bool = False) -> float:
        if real:
            return super().get_phi(x)
        if norm := get_norm(self.coords - x):
            return self.kq / norm
        return np.inf


class Electron(Ball):
    def __init__(
            self,
            pos: tuple[float, float, float] | np.ndarray,
            radius: float = 0.1,
            three_d: bool = True,
            **kwargs
    ):
        super().__init__(pos, radius, three_d, GREEN_D, **kwargs)
        self.seed_x = random.randint(0, 256)
        self.speed_x = randbetween(1, 4)
        self.time_x = 0
        self.seed_y = random.randint(0, 256)
        self.speed_y = randbetween(1, 4)
        self.time_y = 0
        self.add_updater(Electron.updater)

    def updater(self, dt: float):
        self.shift((self.radius/2 * (pnoise1(self.time_x, base=self.seed_x) -
                    pnoise1(self.time_x + self.speed_x*dt, base=self.seed_x)), 0, 0))
        self.time_x += self.speed_x * dt
        self.shift((0, self.radius/2 * (pnoise1(self.time_y, base=self.seed_y) -
                    pnoise1(self.time_y + self.speed_y*dt, base=self.seed_y)), 0))
        self.time_y += self.speed_y * dt


class BarMagnet(VGroup):
    def __init__(self):
        super().__init__(
            Rectangle(2, 1)
            .next_to((0, 0, 0), RIGHT, aligned_edge=LEFT, buff=0)
            .set_fill(RED, 1)
            .set_stroke(RED, 0),
            Text("N", color=RED_E).move_to((1.6, 0, 0)),
            Rectangle(2, 1)
            .next_to((0, 0, 0), LEFT, aligned_edge=RIGHT, buff=0)
            .set_fill(BLUE_D, 1)
            .set_stroke(BLUE_D, 0),
            Text("S", color=BLUE_E).move_to((-1.6, 0, 0))
        )
