__all__ = [
    "ElectronmagneticPair", "ElectronmagneticPairUpdater",
    "ElectronmagneticField", "ElectronmagneticFieldUpdater"
]

from typing import *

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
