__all__ = [
    "ElectronmagneticPair", "ElectronmagneticField"
]

from typing import *

from manimlib import *


class ElectronmagneticPair(VGroup):
    def __init__(
            self,
            coords: Iterable[float],
            e: Sequence[float],
            b: Sequence[float],
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
        self.e = e
        self.b = b
        self.coordinate_system = coordinate_system
        self.e_color = e_color
        self.b_color = b_color
        self.opacity = opacity
        self.vector_config = dict(vector_config)
        origin = coordinate_system.get_origin()
        c2p = coordinate_system.c2p(*coords)
        ec2p = coordinate_system.c2p(*e)
        bc2p = coordinate_system.c2p(*b)
        e_vect = Arrow(
            origin, ec2p, buff=0,
            stroke_color=e_color, stroke_opacity=opacity,
            **vector_config
        )
        b_vect = Arrow(
            origin, bc2p, buff=0,
            stroke_color=b_color, stroke_opacity=opacity,
            **vector_config
        )
        e_vect.shift(c2p - origin)
        b_vect.shift(c2p - origin)
        self.add(e_vect, b_vect)


class ElectronmagneticField(VGroup):
    """adapted from `VectorField`"""
    def __init__(
            self,
            e_func: Callable[[float, float, float], Sequence[float]],
            b_func: Callable[[float, float, float], Sequence[float]],
            coordinate_system: CoordinateSystem,
            step_multiple: float = 0.5,
            e_color: str | Color = GREEN_E,
            b_color: str | Color = BLUE_D,
            opacity: float = 1.,
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
        self.vector_config = dict(vector_config)

        samples = get_sample_points_from_coordinate_system(
            self.coordinate_system, self.step_multiple
        )
        self.add(*(ElectronmagneticPair(
            coords, self.e_func(*coords), self.b_func(*coords), coordinate_system,
            e_color, b_color, opacity, vector_config
        ) for coords in samples))
