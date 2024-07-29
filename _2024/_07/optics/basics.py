"""基础知识篇"""
from _2024._07.optics.scenes import *
from customs.coords import *
from customs.scenes import opening_quote
from customs.utils import *
from manimlib import *


class OpeningQuote(opening_quote.OpeningQuote):
    """tested with commit 259640f5 in osMrPigHead/manimgl"""
    quote_settings = [
        (R"Thoroughly conscious ignorance is the prelude to every real advance in science.",
         R"James C. Maxwell", False, {"ignorance": BLUE}),
        (R"对无知充分的清醒，才是知识真正发展的前奏曲。",
         R"詹姆斯·麦克斯韦", True, {"无知": BLUE})
    ]


class Toc(TocParent):
    """tested with commit 259640f5 in osMrPigHead/manimgl"""
    def construct(self) -> None:
        super().construct()
        self.wait(1)
        self.play(ShowCreation(p1s := SurroundingRectangle(self.p1)))
        self.play(FadeOut(p1s),
                  self.p2.animate.set_color(GREY),
                  self.p3.animate.set_color(GREY),
                  self.p4.animate.set_color(GREY))
        self.wait(6)


class Blackboard(Scene):
    """tested with commit 259640f5 in osMrPigHead/manimgl"""
    def construct(self) -> None:
        pass


class CoulombsLaw(Scene):
    """tested with commit 7766b22a in osMrPigHead/manimgl
    换版本是因为旧版的 TrueDot 真的太丑了"""
    charge_radius = 0.3

    def construct(self) -> None:
        q1 = (TrueDot(radius=self.charge_radius, color=RED)
              .make_3d()
              .add(Text("+", color=WHITE))
              .move_to((-2, 0, 0)))
        q2 = (TrueDot(radius=self.charge_radius, color=RED)
              .make_3d()
              .add(Text("+", color=WHITE))
              .move_to((2, 0, 0)))
        force1 = Arrow(q1.get_center(), q1.get_center() - (1.5, 0, 0), buff=0, stroke_color=YELLOW)
        force1tex = (Tex(R"F", color=YELLOW)
                     .next_to(force1, UP, aligned_edge=DOWN))
        force2 = Arrow(q2.get_center(), q2.get_center() + (1.5, 0, 0), buff=0, stroke_color=YELLOW)
        force2tex = (Tex(R"F", color=YELLOW)
                     .next_to(force2, UP, aligned_edge=DOWN))
        figure = Group(force1, force1tex, force2, force2tex, q1, q2)
        self.add(q1, q2)
        self.wait(1)

        self.remove(q1, q2)
        self.add(force1, force2, force1tex, force1tex)
        self.add(q1, q2)
        self.play(Write(force1), Write(force2), Write(force1tex), Write(force2tex))
        self.wait(2)
        force1tex.add_updater(lambda mob: mob.next_to(force1, UP, aligned_edge=DOWN))
        force2tex.add_updater(lambda mob: mob.next_to(force2, UP, aligned_edge=DOWN))
        self.play(Transform(q2, TrueDot(radius=self.charge_radius, color=BLUE)
                            .make_3d()
                            .add(Text("–", color=WHITE))
                            .move_to((2, 0, 0))),
                  force1.animate.put_start_and_end_on(q1.get_center(), q1.get_center() + (1.5, 0, 0)),
                  force2.animate.put_start_and_end_on(q2.get_center(), q2.get_center() - (1.5, 0, 0)),
                  run_time=1.4)
        self.wait(1)
        title = Text("静电力", font_size=56).to_edge(UP)
        self.play(Write(title))
        self.wait(1.5)

        coulombs_law = Tex(
            R"\vec{F}_{12} = k {q_1 q_2 \over r_{12}^2} \vec{e}_{r12}"
        ).move_to((0, -1, 0)).use_winding_fill(False)
        self.play(FadeTransform(title, Text("库仑定律", font_size=56).to_edge(UP)),
                  figure.animate.shift((0, 1.5, 0)),
                  Write(coulombs_law))
        self.wait(2)
        self.play(ShowPassingFlashAround(coulombs_law[R"q_1 q_2"]))
        self.play(Write(TexText(R"\small C\;(库仑)", color=YELLOW)
                        .next_to(coulombs_law[R"q_1 q_2"], UR, aligned_edge=DL)))
        self.wait(1)
        self.play(ShowPassingFlashAround(coulombs_law[R"\vec{F}_{12}"]))
        self.wait(1)
        self.play(ShowPassingFlashAround(coulombs_law[R"\vec{e}_{r12}"]))
        self.wait(1)
        self.play(ShowPassingFlashAround(coulombs_law[R"k"]))
        self.play(Write(k_tex := TexText(R"\footnotesize 静电力常量", color=YELLOW)
                        .next_to(coulombs_law[R"k"], DOWN, aligned_edge=UP, buff=0.75)))
        self.wait(1)
        self.play(TransformMatchingTex(coulombs_law, coulombs_law := Tex(
            R"\vec{F}_{12} = {1 \over 4 \pi \varepsilon_0} {q_1 q_2 \over r_{12}^2} \vec{e}_{r12}"
        ).move_to((0, -1, 0)), key_map={R"k": R"{1 \over 4 \pi \varepsilon_0}"}, run_time=1),
                  FadeTransform(k_tex, TexText(R"\footnotesize 真空介电常量", color=YELLOW)
                                .next_to(coulombs_law[R"\varepsilon_0"], DOWN, aligned_edge=UP)
                                .use_winding_fill(False)))
        self.wait(2)
        self.play(ApplyWave(coulombs_law[R"q_1 q_2"]))
        self.wait(1)
        self.play(ApplyWave(coulombs_law[R"r_{12}^2"]))
        self.wait(3)

        self.play(Transform(q1, TrueDot(radius=DEFAULT_DOT_RADIUS, color=RED)
                            .make_3d()
                            .add(Text("", color=WHITE))
                            .move_to((-2, 1.5, 0))),
                  Transform(q2, TrueDot(radius=DEFAULT_DOT_RADIUS, color=BLUE)
                            .make_3d()
                            .add(Text("", color=WHITE))
                            .move_to((2, 1.5, 0))))
        self.wait(3)
        points = [q1.get_center().copy()]
        for i in range(3):
            for j in range(3):
                points += [points[-1] + coord(fullrand(0.2), fullrand(0.2))]
            self.play(MoveAlongPath(q1, CubicBezier(*points[-4:]), run_time=0.6))
        for i in range(2):
            points += [points[-1] + coord(fullrand(0.2), fullrand(0.2))]
        points += [points[0]]
        self.play(MoveAlongPath(q1, CubicBezier(*points.copy()[-4:]), run_time=0.6))
        self.wait(1)
