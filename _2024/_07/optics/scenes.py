__all__ = [
    "WavePropagation"
]

from typing import *

from _2024._07.optics.mobject import *
from manimlib import *


class WavePropagation(Scene):
    """tested with commit 88df1dca in osMrPigHead/manimgl"""
    omega = PI / 4
    eb_time = 10
    phi = omega * eb_time

    x_range = (-4, 4, 1)
    y_range = (-3, 3, 1)
    z_range = (-6, 6, 1)
    opacity_dest = 0.4
    opacity_time = (2, 4)
    camera_eular_angles = (-PI*5/6, PI/6, PI*5/6)

    def construct(self) -> None:
        self.camera.frame.set_euler_angles(*self.camera_eular_angles)
        zm = self.z_range[1]
        axes_display = ThreeDAxes(self.x_range, self.y_range, self.z_range,
                                  axis_config={"include_tip": True})
        axes_field = ThreeDAxes((-0, 0.1, 1), (-0, 0.1, 1), self.z_range,
                                axis_config={"include_tip": True})
        field = ElectronmagneticField(
            lambda x, y, z: self.e_wave(z) if x == 0 and y == 0 else (0, 0, 0),
            lambda x, y, z: self.b_wave(z) if x == 0 and y == 0 else (0, 0, 0),
            axes_field
        )
        front_vect = ElectronmagneticPair(
            (0, 0, zm), self.e_wave(zm), self.b_wave(zm), axes_field
        )
        self.add(axes_display, field)

        self.play(UpdateFromAlphaFunc(
            field, lambda mob, alpha: mob.become(ElectronmagneticField(
                lambda x, y, z: self.e_wave(z - alpha * self.phi)
                if x == 0 and y == 0 else (0, 0, 0),
                lambda x, y, z: self.b_wave(z - alpha * self.phi)
                if x == 0 and y == 0 else (0, 0, 0),
                axes_field, opacity=1 - (1-self.opacity_dest)*squish_rate_func(
                    smooth,
                    self.opacity_time[0]/self.eb_time,
                    self.opacity_time[1]/self.eb_time
                )(alpha)
            )), rate_func=linear, run_time=self.eb_time
        ), UpdateFromAlphaFunc(
            front_vect, lambda mob, alpha: mob.become(ElectronmagneticPair(
                (0, 0, zm),
                self.e_wave(zm - alpha * self.phi),
                self.b_wave(zm - alpha * self.phi),
                axes_field
            )), rate_func=linear, run_time=self.eb_time
        ))

    def e_wave(self, z: float) -> Sequence[float]:
        return math.sin(z), 0, 0

    def b_wave(self, z: float) -> Sequence[float]:
        return 0, math.sin(z), 0
