"""基础知识篇"""
from _2024._07.optics.scenes import *
from customs.constants import *
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
                            .add(Text(EN_DASH, color=WHITE))
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


class BlackboardEField(Scene):
    """tested with commit 259640f5 in osMrPigHead/manimgl"""
    def construct(self) -> None:
        # self.add(Rectangle(FRAME_WIDTH/2, FRAME_HEIGHT).to_edge(LEFT, buff=0))  # 答题卡裁切线 (bushi

        coulombs_law_title = Text("库仑定律:", font_size=36).to_edge(UL, buff=0.5)
        coulombs_law = Tex(
            R"\vec{F}_{12} = {1 \over 4 \pi \varepsilon_0} {q_0 q \over r^2} \vec{e}_{r}"
        ).scale(0.75).next_to(coulombs_law_title, RIGHT, aligned_edge=LEFT, buff=1)
        self.add(coulombs_law_title, coulombs_law)
        self.wait()
        self.play(ShowCreationThenFadeAround(coulombs_law[R"q"]))
        self.wait()

        e_field_intensity_title = (Text("电场强度:", font_size=36)
                                   .next_to(coulombs_law_title, DOWN, aligned_edge=UP, buff=0.8))
        e_field_intensity = Tex(
            R"\vec{E} = {\vec{F} \over q} = {1 \over 4 \pi \varepsilon_0} {q_0 \over r^2} \vec{e}_{r}"
        ).scale(0.75).next_to(e_field_intensity_title, RIGHT, aligned_edge=LEFT, buff=1)
        f_qe = Tex(
            R"\vec{F} = q \vec{E}"
        ).scale(0.75).next_to(e_field_intensity_title, DOWN, aligned_edge=UP, buff=0.6)
        self.play(Write(e_field_intensity_title))
        self.play(Write(e_field_intensity[R"\vec{E} = {\vec{F} \over q}"]))
        self.wait()
        self.play(TransformFromCopy(
            coulombs_law[R"= {1 \over 4 \pi \varepsilon_0} {q_0 q \over r^2} \vec{e}_{r}"],
            e_field_intensity[R"= {1 \over 4 \pi \varepsilon_0} {q_0 \over r^2} \vec{e}_{r}"],
            path_arc=2,
            path_arc_axis=IN,
            run_time=2
        ))
        self.wait()
        self.play(Write(f_qe))
        self.wait()


class EField(Scene):
    """tested with commit 656f98fd in osMrPigHead/manimgl"""
    source_charge_radius = 0.3
    probe_charge_radius = 0.2
    kq = 8

    def construct(self) -> None:
        axes = Axes()
        q_source = (TrueDot(radius=self.source_charge_radius, color=RED)
                    .make_3d()
                    .add(Text("+", color=WHITE))
                    .move_to(axes.c2p(0, 0)))
        q_probe = (TrueDot(radius=self.probe_charge_radius, color=RED)
                   .make_3d()
                   .add(Text("+", font_size=36, color=WHITE))
                   .move_to(axes.c2p(3, 2)))

        def get_e(coords: np.ndarray | tuple[float, float]) -> np.ndarray:
            if norm := get_norm(coords):
                return self.kq / norm**2 * normalize(coords)
            return np.array((0, 0))

        force = (Arrow(LEFT, RIGHT, stroke_color=YELLOW)
                 .add_updater(lambda mob: (mob.put_start_and_end_on(
                     rq := q_probe.get_center(), rq + get_e(rq)))))
        field = VectorField(lambda x, y: (0, 0), axes)

        self.add(axes, field, q_source, force, q_probe)
        self.play(MoveAlongPath(q_probe,
                                CubicBezier(axes.c2p(3, 2), axes.c2p(0, 4),
                                            axes.c2p(-3, 2), axes.c2p(-3, -2)),
                                run_time=3, rate_func=linear))
        self.play(field.animate.become(VectorField(lambda x, y: get_e(np.array((x, y)))/4, axes)))
        title = Text("电场", font_size=56).to_edge(UP)
        self.play(FadeIn(title_back := BackgroundRectangle(title)), Write(title))
        asl = AnimatedStreamLines(StreamLines(
            lambda x, y: (x * 0.7 + y * 0.5, y * 0.7 - x * 0.5),
            axes,
            magnitude_range=(0.5, 5)
        ))
        self.add(asl)
        self.wait(5)
        self.play(FadeOut(asl))

        backs = [BackgroundRectangle(mob) for mob in [axes, field, force, q_probe]]
        self.remove(axes, field, q_source, force, q_probe)
        self.add(axes, backs[0], field, backs[1], q_source,
                 force, backs[2], q_probe, backs[3], title_back, title)
        self.play(*(FadeIn(mob) for mob in backs))
        self.wait()
        self.play(FadeOut(backs[1]))
        self.wait()
        self.play(FadeOut(backs[3]))
        self.wait()
        self.play(FadeOut(backs[2]))
        self.wait()
        self.play(FadeOut(backs[0]))
        self.wait()

        # Blackboard 分屏
        # self.add(Rectangle(FRAME_WIDTH/2, FRAME_HEIGHT))  # 答题卡裁切线 (bushi
        self.play(MoveAlongPath(q_probe, Line(axes.c2p(-3, -2), axes.c2p(-2, -2))))
        self.wait()
        self.play(WiggleOutThenIn(force))


class UniformEField(Scene):
    """tested with commit 259640f5 in osMrPigHead/manimgl"""
    kq = 2

    def construct(self) -> None:
        axes = Axes()
        positive_board = VGroup(
            Rectangle(6, 0.5, color=RED, fill_opacity=1),
            Text("+", color=WHITE),
            Text("+", color=WHITE).shift((-1, 0, 0)),
            Text("+", color=WHITE).shift((1, 0, 0)),
            Text("+", color=WHITE).shift((-2, 0, 0)),
            Text("+", color=WHITE).shift((2, 0, 0))
        ).to_edge(UP, buff=2)
        negative_board = VGroup(
            Rectangle(6, 0.5, color=BLUE, fill_opacity=1),
            Text(EN_DASH, color=WHITE),
            Text(EN_DASH, color=WHITE).shift((-1, 0, 0)),
            Text(EN_DASH, color=WHITE).shift((1, 0, 0)),
            Text(EN_DASH, color=WHITE).shift((-2, 0, 0)),
            Text(EN_DASH, color=WHITE).shift((2, 0, 0))
        ).to_edge(DOWN, buff=2)
        bound_board_c = axes.p2c(bound_board := positive_board.get_right())
        ur = CCVector(bound_board_c[0], bound_board_c[1])
        ul = CCVector(-bound_board_c[0], bound_board_c[1])
        dr = CCVector(bound_board_c[0], -bound_board_c[1])
        dl = CCVector(-bound_board_c[0], -bound_board_c[1])
        field = VectorField(lambda x, y: (0, 0), axes)
        self.add(field, positive_board, negative_board)
        self.wait()
        self.play(field.animate.become(VectorField(lambda x, y: (
            self.kq / (ur.y - y) * (sin(~((r := CCVector(x, y)) - ur)) - sin(~(r - ul))) -
            self.kq / (dr.y - y) * (sin(~(r - dr)) - sin(~(r - dl))),
            self.kq / (ur.y - y) * (cos(~(r - ul)) - cos(~(r - ur))) -
            self.kq / (dr.y - y) * (cos(~(r - dl)) - cos(~(r - dr)))
        ), axes)))
        self.wait()
        self.play(ShowCreationThenFadeOut(Rectangle(
            bound_board[0]*1.2, bound_board[1]*2, color=YELLOW
        )))
        self.wait()
        title = Text("匀强电场", font_size=56).to_edge(UP)
        self.play(FadeIn(BackgroundRectangle(title)), Write(title))
        self.wait()
