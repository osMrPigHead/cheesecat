"""引入和目录部分"""
from typing import *

from _2024._07.optics.animation import *
from _2024._07.optics.light import *
from _2024._07.optics.mobject import *
from _2024._07.optics.scenes import *
from customs.scenes import opening_quote
from customs.coords import *
from customs.utils import *
from manimlib import *


class OpeningQuote(opening_quote.OpeningQuote):
    """tested with commit 6d69b8fe in osMrPigHead/manimgl"""
    quote_settings = [
        (R"It is a universal condition of the enjoyable that the mind must believe in the existence of a law, and yet "
         R"have a mystery to move about in.", R"James C. Maxwell", False, {"mystery": BLUE}),
        (R"欢愉的普遍之道在于，相信真理的存在，而始终葆有神秘与好奇。", R"詹姆斯·麦克斯韦", True, {"神秘与好奇": BLUE})
    ]


class QuestionsGeometricalOptic(Scene):
    """tested with commit 6d69b8fe in osMrPigHead/manimgl"""
    def construct(self) -> None:
        self.add(glass := Rectangle(FRAME_WIDTH, 4/9*FRAME_HEIGHT,
                                    color=BLUE_E, fill_opacity=0.4, stroke_opacity=0)
                 .to_edge(DOWN, buff=0))

        anims = []
        time_last = 0
        for _ in range(4):
            anims += (anim := transmit_light_flash_(
                *light_from_path((fullrand(), 1), (fullrand(0.2), -1/9)),
                ((-1, -1/9), (1, -1/9)), 4/3, time_start=time_last
            ))[0]
            time_last = anim[1] + fullrand(0.4)
        self.play(*anims)
        self.wait(2)

        self.play((Rectangle(FRAME_WIDTH, 1e-4,
                             color=TEAL_E, fill_opacity=0.4, stroke_opacity=0)
                   .next_to(glass, UP, buff=0))
                  .animate.set_height(FRAME_HEIGHT/36, stretch=True, about_edge=DOWN),
                  ShowCreation(arrow := Arrow(coord(-3/4, 1/4), coord(-2/3, -1/12))),
                  Write(Text("增透膜")
                        .move_to(arrow.get_start() + coord(0, 1/18), DOWN)),
                  run_time=0.7)
        anims = []
        time_last = 0
        for _ in range(2):
            anims += (anim := transmit_light_flash_(
                p := (1/4 + fullrand(0.2), 1/2 + fullrand(0.2)), -1-1.3j+fullrand(0.1)+fullrand(0.1j),
                ((-1, -1/9), (1, -1/9)), reverse=True, time_start=time_last
            ))[0]
            anims += transmit_light_flash(
                p, -1-1.8j+fullrand(0.1)+fullrand(0.1j),
                ((-1, -1/18), (1, -1/18)), reverse=True, time_end=anim[1]
            )
            anims += [Flash(coord(p), run_time=anim[1] + 0.7,
                            time_span=(anim[1] - WIDTH_RATE, anim[1] - WIDTH_RATE + 0.7))]
            time_last = anim[1] - WIDTH_RATE + 0.7 + fullrand() * 0.4
        self.play(*anims)
        self.play(*list(zip(*transmit_light_path(
            (1/4, 1/2), -1-1.5j,
            ((-1, -1/9), (1, -1/9)), 4/3, reverse=True, reflect_dashed=True
        )))[0])
        self.wait(2)


class QuestionsPolarization(Scene):
    """tested with commit 6d69b8fe in osMrPigHead/manimgl"""
    wave_number = 1
    omega = PI / 4
    eb_time = 10
    rotate_speed = 0.05

    def construct(self) -> None:
        self.add(Text("*此场景有借鉴 3Blue1Brown", font_size=36).to_edge(DOWN, buff=0.1).fix_in_frame())
        # 为什么不用欧拉角? 因为我不会 (bushi
        # 这样写更直观不是么 (
        self.camera.frame.rotate(PI / 12, axis=LEFT)
        self.camera.frame.rotate(PI / 6, axis=DOWN)

        axes_display = ThreeDAxes((-4, 4, 1), (-3, 3, 1), (-6, zm := 6, 1),
                                  axis_config={"include_tip": True})
        axes_display.shift(-axes_display.get_origin())
        axes_field = ThreeDAxes((0, 0.1, 1), (0, 0.1, 1), (-6, 6, 1))
        axes_field.shift(-axes_field.get_origin())
        field = ElectronmagneticFieldUpdater(
            lambda t: lambda x, y, z: (0, math.sin(self.wave_number * z - self.omega * t), 0)
            if x == 0 and y == 0 else (0, 0, 0),
            lambda t: lambda x, y, z: (math.sin(self.wave_number * z - self.omega * t), 0, 0)
            if x == 0 and y == 0 else (0, 0, 0),
            axes_field
        ).add_updater(lambda mob: mob.set_opacity(
            1 - (1-0.4) * smooth(clip(mob.time-3, 0, 1.5) / 1.5)
        ))
        front_pair = ElectronmagneticPairUpdater(
            (0, 0, zm),
            lambda t: (0, math.sin(self.wave_number * zm - self.omega * t), 0),
            lambda t: (math.sin(self.wave_number * zm - self.omega * t), 0, 0),
            axes_field
        )
        self.camera.frame.add_updater(lambda mob, dt: mob.rotate(self.rotate_speed * dt, axis=UP))

        self.add(axes_display, field, front_pair)
        self.wait(15)


class Toc(TocParent):
    """tested with commit 259640f5 in osMrPigHead/manimgl"""
    charge_radius = 0.4
    charge_force = np.array((1, 0, 0))
    accelerate = np.array((0.3, 0, 0))

    def construct(self) -> None:
        self.play(Write(self.title, run_time=1.2),
                  ShowCreation(self.underline, run_time=1.4))

        self.p1demo()
        self.p2demo()
        self.p3demo()
        self.p4demo()
        self.wait(7)

    def p1demo(self) -> None:
        q1 = (TrueDot(color=RED, radius=self.charge_radius, glow_factor=0.4)
              .add(Text("+", color=WHITE))
              .to_edge(LEFT, buff=2))
        q2 = (TrueDot(color=BLUE, radius=self.charge_radius, glow_factor=0.4)
              # 什么? 这不是减号, 这是 en dash, 它遇水变大变高 (雾
              .add(Text("–", color=WHITE))
              .to_edge(RIGHT, buff=2))
        self.play(FadeIn(self.p1, self.p_shift), FadeIn(q1), FadeIn(q2))

        # 7s in total
        force = Arrow(q1.get_right(), q1.get_right() + self.charge_force, stroke_color=YELLOW, buff=0)
        force_tex = Tex(R"\boldmath F", color=YELLOW).next_to(force, UR, aligned_edge=DR)
        # 0-1s
        self.play(ShowCreation(force), Write(force_tex))
        # 1-2s
        self.wait(1)
        t = 0

        def accelerate(mob, dt):
            nonlocal t
            mob.shift(self.accelerate * (t := t + dt) * dt)

        q1.add_updater(accelerate)
        force.add_updater(accelerate)
        force_tex.add_updater(accelerate)
        # 2-4s
        self.wait(2)

        b_arrows = [
            Arrow((-3, -0.35, 0.5+2**0.5/2), (-3, 0.35, 0.5+2**0.5/2),
                  buff=0, stroke_color=BLUE)
            .rotate(PI/4 * n, axis=LEFT, about_point=(-3, 0, 0)) for n in range(8)
        ]
        # 4-5.6s
        self.play(*(FadeIn(b_arrow, time_span=(t_*0.1, t_*0.1+0.8))
                    for b_arrow, t_ in zip(b_arrows, range(8))),
                  Write(b_tex := Tex(R"\boldmath B", color=BLUE_D)
                        .to_edge(LEFT, buff=3)))
        # 5.6-6s
        self.wait(0.4)

        # 6-7s
        self.play(*(FadeOut(mob) for mob in [q1, q2, force, force_tex, b_tex] + b_arrows))

    def p2demo(self) -> None:
        self.camera.frame.rotate(PI/12, axis=LEFT)
        self.camera.frame.rotate(PI/6, axis=DOWN)
        axes = ThreeDAxes((-4, 4, 1), (-3, 3, 1), (-3, 3, 1),
                          axis_config={"include_tip": True}, z_axis_config={"include_tip": True})
        axes.shift(-axes.get_origin())
        field = ElectronmagneticFieldUpdater(
            lambda t: lambda x, y, z: (0, 1-math.cos((t - 1)*2*PI/5.5), 0)
            if t > 1 and y == 0 and get_norm((x, z)) <= 1 else (0, 0, 0),
            lambda t: lambda x, y, z: npcross(UP*math.sin((t - 1)*2*PI/5.5), normalize((x, y, z)))
            / get_norm((x, z))
            if t > 1 and -0.5 <= y <= 0.5 and 1 <= get_norm((x, z)) <= 1.5 else (0, 0, 0),
            axes,
            opacity=0.5
        )
        self.add(field)
        self.play(ShowCreation(axes), FadeIn(self.p2, self.p_shift))

        # 7s in total
        # 0-2.75s
        self.wait(2.75)
        field.set_e_func_t(
            lambda t: lambda x, y, z: (0, 1-math.cos((t - 1)*2*PI/5.5), 0)
            if y == 0 and get_norm((x, z)) <= 1 else
            (0, math.sin((t - 1)*2*PI/5.5) / get_norm((x, z)), 0)
            if -0.5 <= y <= 0.5 and 1.5 <= get_norm((x, z)) <= 2 else (0, 0, 0)
        )
        # 2.75-5.5s
        self.wait(2.75)
        self.remove(field)
        # 5.5-6s
        self.wait(0.5)
        self.play(Uncreate(axes))
        self.camera.frame.to_default_state()

    def p3demo(self) -> None:
        self.camera.frame.rotate(PI / 6, axis=LEFT)
        self.camera.frame.rotate(PI / 4, axis=DOWN)
        slits = SGroup(Prism(width=0.2, height=0.8, depth=0.2, color=BLACK),
                       Prism(width=0.2, height=0.8, depth=1.1, color=BLACK)
                       .move_to((0, 0, -0.3), aligned_edge=OUT),
                       Prism(width=0.2, height=0.8, depth=1.1, color=BLACK)
                       .move_to((0, 0, 0.3), aligned_edge=IN),
                       Prism(width=0.2, height=0.6, depth=2.8, color=BLACK)
                       .move_to((0, 0.4, 0), aligned_edge=DOWN),
                       Prism(width=0.2, height=0.6, depth=2.8, color=BLACK)
                       .move_to((0, -0.4, 0), aligned_edge=UP))
        glow = GlowDot((-4, 0, 0), radius=0.4)
        # 调整图层顺序
        self.remove(self.p1, self.p2)
        self.add(slits, glow)
        self.add(self.p1, self.p2)
        self.play(ShowCreation(slits), FadeIn(glow), FadeIn(self.p3, self.p_shift))

        # 8s in total
        # 0-2.5s
        self.play(XZBroadcast(glow.get_center(), big_radius=4.2, color=YELLOW, run_time=2.5))
        # 2.5-5s
        self.play(XZBroadcast((0, 0, -0.15), big_radius=4.2, color=YELLOW, run_time=2.5),
                  XZBroadcast((0, 0, 0.15), big_radius=4.2, color=YELLOW))
        image = (ImageMobject("optics/screen.png", height=0.4)
                 .move_to((4, 0, 0)).rotate(PI/2, UP))
        # 5-6s
        self.play(FadeIn(image))
        # 6-7s
        self.wait(1)
        self.play(*(FadeOut(mob) for mob in [slits, glow, image]))
        self.camera.frame.to_default_state()

    def p4demo(self) -> None:
        axes = Axes((-4, 4, 1), (-2, 3, 1))
        field = ElectronmagneticFieldUpdater(
            lambda t: lambda x, y: (math.sin(t-1)*(2/3 if y > 0 else 1/2), 0)
            if t > 1 else (0, 0),
            lambda t: lambda x, y: (0, 0),
            axes,
            step_multiple=1
        )

        charge_time = 0

        def charge_updater(mob, dt):
            nonlocal charge_time
            mob.shift(((-math.sin(charge_time)+math.sin(charge_time := charge_time + dt))/3, 0, 0))

        charges = Group(*(
            TrueDot(color=BLUE, radius=self.charge_radius/2, glow_factor=0.4)
            .add(Text("–", font_size=24, color=WHITE))
            .move_to(axes.c2p(x+0.5, 0, 0))
            for x in range(-4, 4, 1)
        )).add_updater(charge_updater)
        self.add(field)
        # 调整图层顺序
        self.remove(self.p1, self.p2, self.p3)
        self.add(axes, charges)
        self.add(self.p1, self.p2, self.p3)
        self.play(ShowCreation(axes), FadeIn(charges), FadeIn(self.p4, self.p_shift))
        self.wait(3*PI)
        self.remove(field)
        self.play(*(FadeOut(mob) for mob in [axes, charges]))


class ComingSoon(Scene):
    """tested with commit 259640f5 in osMrPigHead/manimgl"""
    def construct(self) -> None:
        self.play(Write(Text("敬请期待", font_size=144), run_time=6))
        self.wait(1)
