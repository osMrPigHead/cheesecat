"""基础知识篇 Part 2: 电磁感应"""
import random

from _2024._07.optics.mobject import *
from cc_config import *
from customs.utils import *
from manimlib import *


class DynamicEMF(Scene):
    """tested with commit 656f98fd in osMrPighead/manimgl"""
    def construct(self) -> None:
        xxxxxx114514 = (VGroup(*(Text("+", font_size=20, color=BLUE_D)
                               .rotate(PI/4)
                               .move_to((x, y + 0.5, 0))
                                 for x in range(-8, 8) for y in range(-5, 5))))
        line = (Cylinder(radius=0.1, height=20)
                .rotate(PI/2, RIGHT)
                .move_to((-5, 0, 0))
                .add_updater(lambda mob, dt: mob.shift((dt/4, 0, 0))))
        b_tex = Tex(R"B", color=BLUE_D).to_edge(UL)
        v_arrow = (Arrow(LEFT, RIGHT, stroke_color=YELLOW, buff=0)
                   .add_updater(lambda mob: mob.put_start_and_end_on(
                       line.get_center(),
                       line.get_center() + (1, 0, 0)
                   )))
        v_tex = Tex(R"v", color=YELLOW).add_updater(lambda mob: mob.next_to(v_arrow, UP))
        i_arrow = (Arrow(DOWN, UP, stroke_color=BLUE_D, buff=0)
                   .add_updater(lambda mob: mob.next_to(line, LEFT)))
        i_tex = Tex(R"I", color=BLUE_D).add_updater(lambda mob: mob.next_to(i_arrow, LEFT))
        self.add(xxxxxx114514, line)
        self.wait()
        self.play(Write(i_arrow), Write(i_tex))
        self.wait()
        self.remove(line)
        self.add(v_arrow, line)
        self.play(FadeIn(BackgroundRectangle(b_tex)), Write(b_tex),
                  Write(v_arrow), Write(v_tex))
        self.wait()
        e1 = (Charge(ORIGIN, -1, 0.1, 0)
              .add_updater(lambda mob: mob.move_to(line.get_center() + (-0.02*line.get_center()[0], 0, 0.2))))
        self.play(FadeIn(e1))
        self.wait()
        lorentz_force_arrow1 = (Arrow(LEFT, RIGHT, stroke_color=YELLOW, buff=0)
                                .add_updater(lambda mob: mob.put_start_and_end_on(
                                    e1.get_center(),
                                    e1.get_center() - (0, 1.5, 0)
                                )))
        lorentz_force_tex1 = (Tex(R"-e\vec{v}\times\vec{B}", color=YELLOW)
                              .scale(0.8)
                              .add_updater(lambda mob: mob.next_to(e1.get_center() - (0, 1.5, 0), RIGHT)))
        self.remove(e1)
        self.add(lorentz_force_arrow1, e1)
        self.play(Write(lorentz_force_arrow1), Write(lorentz_force_tex1))
        self.wait()
        e1.clear_updaters()
        f = color_by_z([BLUE, RED], -6, 6)
        self.play(UpdateFromAlphaFunc(
            e1, lambda mob, alpha: mob.move_to(line.get_center() + (-0.02*line.get_center()[0], -8*alpha, 0.2))
        ), line.animate.set_color_by_rgb_func(lambda p: f((p[0], p[2], p[1]))))
        self.wait()
        e_arrow = (Arrow(LEFT, RIGHT, stroke_color=GREEN, buff=0)
                   .add_updater(lambda mob: mob.put_start_and_end_on(
                       line.get_center() + (0, 0.5, 0),
                       line.get_center() - (0, 0.5, 0)
                   )))
        e_tex = (Tex(R"\vec{E}", color=GREEN)
                 .add_updater(lambda mob: mob.next_to(line.get_center() - (0, 0.5, 0), RIGHT)))
        self.play(Write(e_arrow), Write(e_tex))
        self.wait()
        e2 = (Charge(ORIGIN, -1, 0.1, 0)
              .add_updater(lambda mob: mob.move_to(line.get_center() + (-0.02*line.get_center()[0], 0, 0.2))))
        lorentz_force_arrow2 = (Arrow(LEFT, RIGHT, stroke_color=YELLOW, buff=0)
                                .add_updater(lambda mob: mob.put_start_and_end_on(
                                    e2.get_center(),
                                    e2.get_center() - (0, 1.5, 0)
                                )))
        lorentz_force_tex2 = (Tex(R"-e\vec{v}\times\vec{B}", color=YELLOW)
                              .scale(0.8)
                              .add_updater(lambda mob: mob.next_to(e2.get_center() - (0, 1.5, 0), RIGHT)))
        self.play(*(FadeIn(mob) for mob in [lorentz_force_arrow2, lorentz_force_tex2, e2]))
        e_force_arrow = Arrow(LEFT, RIGHT, stroke_color=GOLD, buff=0)
        e_force_tex = (Tex(R"-e\vec{E}", color=GOLD)
                       .scale(0.8)
                       .add_updater(lambda mob: mob.next_to(e_force_arrow.get_end(), RIGHT)))
        self.remove(e2)
        self.add(e_force_arrow, e2)
        self.play(UpdateFromAlphaFunc(e_force_arrow, lambda mob, alpha: mob.put_start_and_end_on(
            e2.get_center(),
            e2.get_center() + (0, 1.5*smooth(alpha), 0)
        ), rate_func=linear, run_time=2), Write(e_force_tex, suspend_mobject_updating=False),
                  *(FadeOut(mob, time_span=(1, 2)) for mob in [i_arrow, i_tex]))
        e_force_arrow.add_updater(lambda mob: mob.put_start_and_end_on(
                                      e2.get_center(),
                                      e2.get_center() + (0, 1.5, 0)
                                  ))
        self.wait()
        line_up = Line(LEFT, RIGHT, stroke_color=YELLOW).add_updater(lambda mob: mob.put_start_and_end_on(
            line.get_center() + (0, 3, 0),
            line.get_center() + (-2, 3, 0)
        ))
        line_down = Line(LEFT, RIGHT, stroke_color=YELLOW).add_updater(lambda mob: mob.put_start_and_end_on(
            line.get_center() + (0, -3, 0),
            line.get_center() + (-2, -3, 0)
        ))
        arrow_up = Arrow(LEFT, RIGHT, stroke_color=YELLOW).add_updater(lambda mob: mob.put_start_and_end_on(
            line.get_center() + (-1.5, 0.5, 0),
            line.get_center() + (-1.5, 3, 0)
        ))
        arrow_down = Arrow(LEFT, RIGHT, stroke_color=YELLOW).add_updater(lambda mob: mob.put_start_and_end_on(
            line.get_center() + (-1.5, -0.5, 0),
            line.get_center() + (-1.5, -3, 0)
        ))
        u_sign = (Tex(R"U", color=YELLOW)
                  .add_updater(lambda mob: mob.move_to(line.get_center() + (-1.5, 0, 0))))
        self.play(*(Write(mob) for mob in [line_up, line_down, arrow_up, arrow_down, u_sign]))
        self.wait()
        ek_arrow = (Arrow(LEFT, RIGHT, stroke_color=GOLD, buff=0)
                    .add_updater(lambda mob: mob.put_start_and_end_on(
                        line.get_center() + (1.5, -0.5, 0),
                        line.get_center() + (1.5, 0.5, 0)
                    )))
        ek_tex = (Tex(R"\vec{E}_k", color=GOLD)
                  .add_updater(lambda mob: mob.next_to(ek_arrow, RIGHT)))
        self.play(Write(ek_arrow), Write(ek_tex))
        self.wait()
        self.play(Transform(lorentz_force_tex2, Tex(R"-e\vec{E}_k", color=YELLOW)
                            .add_updater(lambda mob: mob.next_to(e2.get_center() - (0, 1.5, 0), RIGHT))))
        self.wait()
        title = (Text("动生电动势", font_size=56)
                 .to_edge(UP))
        self.play(FadeIn(BackgroundRectangle(title)), Write(title))
        self.wait()


class DynamicEMFFormula(Scene):
    """tested with commit 259640f5 in osMrPighead/manimgl"""
    def construct(self) -> None:
        dynamic_emf = Tex(R"\mathscr{E}=-Blv").to_edge(DL)
        self.play(FadeIn(BackgroundRectangle(dynamic_emf)), Write(dynamic_emf))
        self.wait()


class InducedEMFLeadin(Scene):
    """tested with commit 259640f5 in osMrPighead/manimgl"""
    def construct(self) -> None:
        xxxxxx114514 = (VGroup(*(Text("+", font_size=20, color=BLUE_D)
                               .rotate(PI / 4)
                               .move_to((x, y + 0.5, 0))
                                 for x in range(-16, 16) for y in range(-10, 10))))
        line = Torus(r1=2, r2=0.15)
        self.add(xxxxxx114514, line)
        self.wait()
        self.play(xxxxxx114514.animate.become(VGroup(*(Text("+", font_size=20, color=BLUE_D)
                                                     .rotate(PI / 4)
                                                     .move_to((x/2, (y + 0.5)/2, 0))
                                                       for x in range(-16, 16) for y in range(-10, 10)))))
        self.wait()
        i_arrow = Arc(PI*2/3, -PI/3, 1.6).set_color(BLUE_D).add_tip()
        i_tex = Tex(R"I", color=BLUE_D).next_to(i_arrow, DOWN)
        self.play(Write(i_arrow), Write(i_tex))
        self.wait()
        title = (Text("感生电动势", font_size=56)
                 .to_edge(UP))
        self.play(FadeIn(BackgroundRectangle(title)), Write(title))
        self.wait()
        e_arrow = Arc(-PI/3, -PI/3, 1.6).set_color(GREEN).add_tip()
        e_tex = Tex(R"E", color=GREEN).next_to(e_arrow, UP)
        self.play(Write(e_arrow), Write(e_tex),
                  FadeTransform(title, Text("感生电场", font_size=56)
                  .to_edge(UP)))
        self.wait()


class LenzsLawCorrect(Scene):
    """tested with commit a4210293 in osMrPighead/manimgl"""
    def construct(self) -> None:
        # LenzsLawWrong 分屏
        if DEBUG:
            self.add(Rectangle(FRAME_WIDTH/2, FRAME_HEIGHT))  # 答题卡裁切线 (bushi

        mark = Checkmark().to_edge(DR).shift((-FRAME_X_RADIUS/2, 0, 0)).fix_in_frame()
        self.camera.frame.rotate(PI/12, axis=LEFT)
        self.camera.frame.rotate(PI/6, axis=DOWN)
        line = Torus(r1=1.2, r2=0.15).rotate(PI/2, RIGHT)
        asl_b = AnimatedStreamLines(StreamLines(
            lambda x, y, z: (0, (y+3)/3, 0)
            if get_norm((x, z)) <= 1 else (0, 0, 0),
            ThreeDAxes((-1, 1, 1), (-3, 3, 1), (-1, 1, 1),
                       width=1.6, height=6, depth=1.6)
        ))
        self.add(line, asl_b)
        self.wait()
        asl_e = AnimatedStreamLines(StreamLines(
            lambda x, y: np.array((-y, x)) / get_norm((x, y))**3,
            Axes((-1, 1, 1), (-1, 1, 1), width=1.2, height=1.2).move_to((1.2, 0, 0))
        ))
        e_arrow = (Arc(PI*2/3, -PI/3, 1.4)
                   .set_color(GREEN).add_tip()
                   .rotate(PI/2, RIGHT, ORIGIN).shift((0, -0.5, 0)))
        self.add(asl_e)
        self.play(Write(e_arrow))
        self.wait()
        self.play(Write(mark))
        self.wait()


class LenzsLawWrong(Scene):
    """tested with commit a4210293 in osMrPighead/manimgl"""
    def construct(self) -> None:
        # LenzsLawCorrect 分屏
        if DEBUG:
            self.add(Rectangle(FRAME_WIDTH/2, FRAME_HEIGHT))  # 答题卡裁切线 (bushi

        mark = Exmark().to_edge(DL).shift((FRAME_X_RADIUS/2, 0, 0)).fix_in_frame()
        self.camera.frame.rotate(PI/12, axis=LEFT)
        self.camera.frame.rotate(PI/6, axis=DOWN)
        line = Torus(r1=1.2, r2=0.15).rotate(PI/2, RIGHT)
        asl_b = AnimatedStreamLines(StreamLines(
            lambda x, y, z: (0, (y+3)/3, 0)
            if get_norm((x, z)) <= 1 else (0, 0, 0),
            ThreeDAxes((-1, 1, 1), (-3, 3, 1), (-1, 1, 1),
                       width=1.6, height=6, depth=1.6)
        ))
        self.add(line, asl_b)
        self.wait()
        asl_e = AnimatedStreamLines(StreamLines(
            lambda x, y: np.array((y, -x)) / get_norm((x, y))**3,
            Axes((-1, 1, 1), (-1, 1, 1), width=1.2, height=1.2).move_to((1.2, 0, 0))
        ))
        e_arrow = (Arc(PI/3, PI/3, 1.4)
                   .set_color(GREEN).add_tip()
                   .rotate(PI/2, RIGHT, ORIGIN).shift((0, -0.5, 0)))
        self.add(asl_e)
        self.play(Write(e_arrow))
        self.wait()
        self.play(Write(mark))
        self.wait()


class FaradaysLawView1(Scene):
    """tested with commit a4210293 in osMrPighead/manimgl"""
    def construct(self) -> None:
        # FaradaysLawView2 分屏
        if DEBUG:
            self.add(Rectangle(FRAME_WIDTH/2, FRAME_HEIGHT))  # 答题卡裁切线 (bushi

        xxxxxx114514 = (VGroup(*(Text("+", font_size=20, color=BLUE_D)
                               .rotate(PI / 4)
                               .move_to((x, y + 0.5, 0))
                                 for x in range(-16, 16) for y in range(-10, 10))))
        line = (SVGMobject("optics/casual_coil.svg")
                .scale(1.5).set_stroke(WHITE, 4).set_fill(opacity=0))
        line.move_to(-line.get_center_of_mass())
        tex = Tex(R"B S").shift((-0.4, 0, 0))
        self.add(xxxxxx114514, line)
        self.wait()
        self.play(Write(tex[R"S"]))
        self.play(xxxxxx114514.animate.become(VGroup(*(Text("+", font_size=20, color=BLUE_D)
                                                     .rotate(PI / 4)
                                                     .move_to((x*2/3, (y + 0.5)*2/3, 0))
                                                       for x in range(-16, 16) for y in range(-10, 10)))))
        self.wait()
        self.play(Write(tex[R"B"]))
        self.wait()
        self.play(TransformMatchingTex(tex, Tex(R"S \Delta B").shift((-0.4, 0, 0)),
                                       path_arc=1, path_arc_axis=IN))
        self.wait()
        self.play(xxxxxx114514.animate.become(VGroup(*(Text("+", font_size=20, color=BLUE_D)
                                                     .rotate(PI / 4)
                                                     .move_to((x/2, (y + 0.5)/2, 0))
                                                       for x in range(-16, 16) for y in range(-10, 10)))))
        self.wait()


class FaradaysLawView2(Scene):
    """tested with commit a4210293 in osMrPighead/manimgl"""
    def construct(self) -> None:
        # FaradaysLawView1 分屏
        if DEBUG:
            self.add(Rectangle(FRAME_WIDTH/2, FRAME_HEIGHT))  # 答题卡裁切线 (bushi

        xxxxxx114514 = (VGroup(*(Text("+", font_size=20, color=BLUE_D)
                               .rotate(PI / 4)
                               .move_to((x*2/3, (y + 0.5)*2/3, 0))
                                 for x in range(-16, 16) for y in range(-10, 10))))
        line = (SVGMobject("optics/casual_coil.svg")
                .scale(1.5).set_stroke(WHITE, 4).set_fill(opacity=0))
        line.shift(-line.get_center_of_mass())
        tex = Tex(R"S \Delta B").shift((-0.4, 0, 0))
        self.add(xxxxxx114514, line, tex)
        self.wait()

        def f(p):
            n = npcross(p - npforward(p), (0, 0, 1))
            nn = sum(n[..., i]**2 for i in range(3))**0.5
            n[nn == 0] = n[npforward(nn) == 0]
            nn[nn == 0] = nn[npforward(nn) == 0]
            return p + (n.T / nn * 0.4).T
        line.generate_target().apply_points_function(f).set_stroke(WHITE, 2)
        self.play(TransformFromCopy(line, line.target))
        self.wait()
        self.play(TransformMatchingTex(tex, Tex(R"B \Delta S").shift((-0.4, 0, 0)),
                                       path_arc=1, path_arc_axis=IN))
        self.wait()
        diffrence = Difference(line.target, line).set_color(PURPLE).set_fill(opacity=0.6)
        self.add(diffrence)
        self.play(fade_update(diffrence, 0.6))
        self.wait()
        rect = Rectangle(5, 0.3).to_edge(DOWN).set_color(PURPLE).set_fill(opacity=0.6)
        self.play(Transform(diffrence, rect))
        self.wait()


class FaradaysLawFormula(Scene):
    """tested with commit a4210293 in osMrPighead/manimgl"""
    def construct(self) -> None:
        evb = Tex(R"\vec{E} = \vec{v} \times \vec{B}").shift((0, 2, 0))
        self.play(FadeIn(BackgroundRectangle(evb)), Write(evb))
        self.wait()
        sdb = Tex(R"B \Delta  S  = S \Delta B").next_to(evb, DOWN, aligned_edge=UP, buff=0.6)
        self.play(FadeIn(BackgroundRectangle(sdb)), Write(sdb))
        self.wait()
        self.play(TransformMatchingTex(
            sdb,
            sdb := Tex(R"B l v \Delta  t = S \Delta B").next_to(evb, DOWN, aligned_edge=UP, buff=0.6),
            key_map={
                R"B ": R"B l v",
                R"\Delta  ": R"\Delta  ",
                R"= S \Delta B": R"= S \Delta B"
            }
        ))
        self.wait()
        self.play(TransformMatchingTex(
            sdb,
            sdb := Tex(R"v B l \Delta t = S \Delta B").next_to(evb, DOWN, aligned_edge=UP, buff=0.6),
            key_map={
                R"B ": R"B ",
                R"l ": R"l ",
                R"v ": R"v ",
                R"\Delta  t = S \Delta B": R"\Delta t = S \Delta B"
            },
            path_arc=2
        ))
        self.wait()
        self.play(TransformMatchingTex(
            sdb,
            sdb := Tex(R"E l \Delta t = S \Delta B").next_to(evb, DOWN, aligned_edge=UP, buff=0.6),
            key_map={
                R"v B": R"E",
                R"l": R"l",
                R" \Delta t = S \Delta B": R" \Delta t = S \Delta B"
            }
        ))
        self.wait()
        self.play(TransformMatchingTex(
            sdb,
            sdb := Tex(R"\mathscr{E} = {S \Delta B \over \Delta t}").next_to(evb, DOWN, aligned_edge=UP, buff=0.6),
            key_map={
                R"E l": R"\mathscr{E}",
                R"\Delta t": R"\Delta t",
                R"S \Delta B": R"S \Delta B"
            }
        ))
        self.wait()
        self.play(TransformMatchingTex(
            sdb,
            Tex(R"\mathscr{E} = -{S \Delta B \over \Delta t}").next_to(evb, DOWN, aligned_edge=UP, buff=0.6),
            key_map={
                R"\mathscr{E} =": R"\mathscr{E} = ",
                R"{S \Delta B \over \Delta t}": R"{S \Delta B \over \Delta t}"
            }
        ))
        self.wait()


class DisplacementCurrent(Scene):
    """tested with commit af8e5236 in osMrPigHead/manimgl"""
    def construct(self) -> None:
        left = Prism(0.2, 3, 2).set_color(GREY).move_to((-3, 0, 0))
        right = Prism(0.2, 3, 2).set_color(GREY).move_to((3, 0, 0))
        self.add(left, right)
        self.wait()
        electrons = Group(*(Electron((-2.8+fullrand(0.1), y*1.4/5, 1.2)) for y in range(-5, 6)))
        self.play(fade_update(electrons, 1))
        self.wait()
        e_arrow = FillArrow(LEFT, RIGHT).set_color(GREEN)
        e_tex = Tex(R"\vec{E}").set_color(GREEN).next_to(e_arrow, DOWN)
        anims = []
        eis = list(range(11))
        for i in range(11):
            ei = random.choice(eis)
            eis.remove(ei)
            electrons[ei].generate_target().set_x(2.8+fullrand(0.1))
            y = electrons[ei].get_y()
            anims += [MoveToTarget(electrons[ei], path_arc=(abs(y)-2)*sgn(y, 1), time_span=(i*0.8, i*0.8+0.6))]

        def updater(mob, alpha):
            t = alpha*8.6
            if 0 <= t % 0.8 <= 0.6:
                beta = t % 0.8 / 0.6
                x = (t//0.8 + smooth(beta))/11
                mob.put_start_and_end_on(x*LEFT, x*RIGHT)
        self.add(e_arrow)
        self.play(UpdateFromAlphaFunc(e_arrow, updater, run_time=8.6, rate_func=linear),
                  *anims, Write(e_tex, time_span=(1, 1.5)))
        self.wait()
        rect = SurroundingRectangle(e_tex)
        rect.shift(0.2*UP).rescale_to_fit(rect.get_height() + 0.5, 1)
        self.play(ShowCreation(rect))
        self.wait()
        i_d_arrow = FillArrow(LEFT*2/3, RIGHT*2/3).set_color(BLUE_D).next_to(e_tex, DOWN)
        i_d_tex = Tex(R"I_d").set_color(BLUE_D).next_to(i_d_arrow, DOWN)
        self.play(Write(i_d_arrow))
        self.wait()
        title = (Text("位移电流", font_size=56)
                 .to_edge(UP))
        self.play(FadeIn(BackgroundRectangle(title)), Write(title), Write(i_d_tex))
        self.wait()
        buff = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER
        left_ = (Prism(0.01, 3, 2)
                 .set_color(BLUE_D).set_opacity(0.6)
                 .next_to(left, LEFT, buff=buff))
        right_ = (Prism(0.01, 3, 2)
                  .set_color(BLUE_D).set_opacity(0.6)
                  .next_to(left, RIGHT, buff=buff))
        self.play(FadeIn(left_, shift=LEFT*buff), FadeIn(right_, shift=RIGHT*buff))
        self.wait()
        self.play(FadeOut(left_, shift=RIGHT*buff), FadeOut(right_, shift=LEFT*buff))
        self.wait()


class DisplacementCurrentFormula(Scene):
    """tested with commit a4210293 in osMrPighead/manimgl"""
    def construct(self) -> None:
        e_arrow = FillArrow(LEFT, RIGHT).set_color(GREEN)
        i_d_formula = (Tex(R"\Delta E = {\Delta q \over \varepsilon_0 S}")
                       .next_to(e_arrow, UP, aligned_edge=DOWN, buff=1))
        self.play(Write(i_d_formula))
        self.wait()
        self.play(TransformMatchingTex(
            i_d_formula,
            i_d_formula := Tex(R"{\Delta E \over \Delta  t} = {\Delta q \over \varepsilon_0 S \Delta t}")
            .next_to(e_arrow, UP, aligned_edge=DOWN, buff=1),
            key_map={
                R"\Delta E": R"\Delta E",
                R"\Delta q": R"\Delta q",
                R"\varepsilon_0 S": R"\varepsilon_0 S"
            }
        ))
        self.wait()
        self.play(TransformMatchingTex(
            i_d_formula,
            Tex(R"{\Delta E \over \Delta  t} = {I_d \over \varepsilon_0 S}")
            .next_to(e_arrow, UP, aligned_edge=DOWN, buff=1),
            key_map={
                R"\Delta E": R"\Delta E",
                R"\Delta  t": R"\Delta  t",
                R"\Delta q": R"I_d",
                R"\varepsilon_0 S": R"\varepsilon_0 S"
            }
        ))
        self.wait()
