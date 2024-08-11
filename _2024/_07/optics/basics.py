"""基础知识篇"""
from _2024._07.optics.animation import *
from _2024._07.optics.calculations import *
from _2024._07.optics.mobject import *
from _2024._07.optics.scenes import *
from customs.constants import *
from customs.coords import *
from customs.scenes import big_question_mark, opening_quote
from customs.utils import *
from manimlib import *


# class OpeningQuote(opening_quote.OpeningQuote):
#     """tested with commit 259640f5 in osMrPigHead/manimgl"""
#     quote_settings = [
#         (R"Thoroughly conscious ignorance is the prelude to every real advance in science.",
#          R"James C. Maxwell", False, {"ignorance": BLUE}),
#         (R"对无知充分的清醒，才是知识真正发展的前奏曲。",
#          R"詹姆斯·麦克斯韦", True, {"无知": BLUE})
#     ]


class OpeningQuote(opening_quote.OpeningQuote):
    """tested with commit 259640f5 in osMrPighead/manimgl"""
    quote_settings = [
        (R"没有昨日的基础科学，就没有今日的技术革命。",
         R"李政道", True, {"基础科学": BLUE, "技术革命": BLUE})
    ]

    def construct(self) -> None:
        self.quotes, self.authors = self.get_quotes_and_authors()
        self.play(*(VFadeIn(quote, run_time=self.run_time_per_char * max(len(quote) for quote, _, _, _
                                                                         in self.quote_settings),
                            lag_ratio=self.lag_ratio) for quote in self.quotes))
        self.wait(2)
        self.play(Write(Text("李政道教授于美国时间8月4日在旧金山因病逝世，以此纪念李教授对物理学作出的卓越贡献",
                             font_size=24).to_edge(DOWN)),
                  *(Write(author, run_time=3) for author in self.authors))
        self.wait(2)


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
    def construct(self) -> None:
        q1 = Charge((-2, 0, 0), 1)
        q2 = Charge((2, 0, 0), 1)
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
        self.play(Transform(q2, Charge((2, 0, 0), -1)),
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

        self.play(Transform(q1,
                            Charge((-2, 1.5, 0), 1, DEFAULT_DOT_RADIUS, 0)),
                  Transform(q2,
                            Charge((2, 1.5, 0), -1, DEFAULT_DOT_RADIUS, 0)))
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


class QProbeCircling(Scene):
    """tested with commit 656f98fd in osMrPigHead/manimgl"""
    q_source_coords = (0, 0)
    q_probe_coords = (3, 2)
    kq = 8

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.axes = Axes()
        self.q_path = CubicBezier(self.axes.c2p(3, 2), self.axes.c2p(0, 4),
                                  self.axes.c2p(-3, 2), self.axes.c2p(-3, -2))
        self.q_run_time = 3

        self.q_source = AxesCharge(self.axes, self.q_source_coords, self.kq)
        self.q_probe = AxesCharge(self.axes, self.q_probe_coords, 1, 0.2, 36)

        self.force = (Arrow(LEFT, RIGHT, stroke_color=YELLOW)
                      .add_updater(lambda mob: (mob.put_start_and_end_on(
                          rq := self.q_probe.get_center(),
                          rq + self.q_source.get_e(rq, True)
                      ))))
        self.field = VectorField(lambda x, y: (0, 0), self.axes)

    def construct(self) -> None:
        self.add(self.axes, self.field, self.q_source, self.force, self.q_probe)
        self.play(MoveAlongPath(self.q_probe, self.q_path,
                                run_time=self.q_run_time, rate_func=linear))


class EField(QProbeCircling):
    """tested with commit 656f98fd in osMrPigHead/manimgl"""
    def construct(self) -> None:
        super().construct()

        self.play(self.field.animate.become(VectorField(
            lambda x, y: self.q_source.get_e((x, y))/4,
            self.axes
        )))
        title = Text("电场", font_size=56).to_edge(UP)
        self.play(FadeIn(title_back := BackgroundRectangle(title)), Write(title))
        asl = AnimatedStreamLines(StreamLines(
            lambda x, y: (x*0.7+y*0.5, y*0.7-x*0.5),
            self.axes,
            magnitude_range=(0.5, 5)
        ))
        self.add(asl)
        self.wait(5)
        self.play(FadeOut(asl))

        backs = [BackgroundRectangle(mob) for mob in
                 [self.axes, self.field, self.force, self.q_probe]]
        self.remove(self.axes, self.field, self.q_source, self.force, self.q_probe)
        self.add(self.axes, backs[0], self.field, backs[1], self.q_source,
                 self.force, backs[2], self.q_probe, backs[3], title_back, title)
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
        if DEBUG:
            self.add(Rectangle(FRAME_WIDTH/2, FRAME_HEIGHT))  # 答题卡裁切线 (bushi
        self.play(MoveAlongPath(self.q_probe, Line(self.axes.c2p(-3, -2),
                                                   self.axes.c2p(-2, -2))))
        self.wait()
        self.play(WiggleOutThenIn(self.force))


class EFieldAnimatedStreamLines(QProbeCircling):
    """tested with commit 656f98fd in osMrPigHead/manimgl"""
    def construct(self) -> None:
        self.add(self.axes, self.field, self.q_source, self.force, self.q_probe)
        self.field.become(VectorField(
            lambda x, y: self.q_source.get_e((x, y)) / 4,
            self.axes
        ))
        self.add(BackgroundRectangle(title := Text("电场", font_size=56).to_edge(UP)), title)
        self.q_probe.move_to(self.axes.c2p(-3, -2))
        asl = AnimatedStreamLines(StreamLines(
            lambda x, y: (x*0.7+y*0.5, y*0.7-x*0.5),
            self.axes,
            magnitude_range=(0.5, 5)
        ))
        self.add(asl)
        self.wait(10)
        self.play(stroke_fade_update(asl, 0, smooth, 1))


class UniformEField(Scene):
    """tested with commit 259640f5 in osMrPigHead/manimgl"""
    kq = 2

    def construct(self) -> None:
        axes = Axes()
        positive_board = VGroup(
            Rectangle(6, 0.5, color=RED, fill_opacity=1),
            *(Text("+").shift((i, 0, 0)) for i in range(-2, 3))
        ).to_edge(UP, buff=2)
        negative_board = VGroup(
            Rectangle(6, 0.5, color=BLUE, fill_opacity=1),
            *(Text(EN_DASH).shift((i, 0, 0)) for i in range(-2, 3))
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


class PotentialLeadin(QProbeCircling):
    """tested with commit 656f98fd in osMrPigHead/manimgl"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field = VectorField(
            lambda x, y: self.q_source.get_e((x, y))/4,
            self.axes
        )

    def construct(self) -> None:
        super().construct()
        self.wait()

        phi = (ParametricSurface(
            lambda u, v: (u, v, self.q_source.get_phi((u, v, 0), True)),
            (self.axes.get_left()[0], self.axes.get_right()[0]),
            (self.axes.get_bottom()[1], self.axes.get_top()[1])
        ).set_color_by_rgb_func(color_by_z((BLUE, RED), -3, 3))
               .set_shading(0, 0, 0))
        title = (Text("电势", weight=BOLD, font_size=56)
                 .to_edge(UP)
                 .fix_in_frame())
        phi_tex = (Tex(R"\Large\boldsymbol\varphi", color=RED_B)
                   .move_to(self.axes.c2p(4, -3))
                   .shift((0, 0, 3))
                   .flip()
                   .rotate(PI/2, axis=RIGHT))

        self.play(
            fade_update(phi, 0.8),
            stroke_fade_update(SurfaceMesh(phi), 0.8),
            camera_update(self, [], [(PI/3, RIGHT, rush_from), (PI/4, OUT, linear)], 1.5),
            Write(title), Write(phi_tex),
            run_time=2
        )
        self.camera.frame.add_updater(lambda mob, dt: mob.rotate(dt*PI/8, axis=OUT))
        self.wait(16)


class Potential(Scene):
    """tested with commit 656f98fd in osMrPigHead/manimgl"""
    def construct(self) -> None:
        source = Ball((-3, 0, 0), 0.4)
        tex_s = (Tex(R"M")
                 .add_updater(lambda mob: mob.next_to(source, UP)))

        def build_probe() -> tuple[Ball, Tex, Arrow]:
            return (probe := Ball((2, 0, 0), 0.2),
                    Tex(R"m").add_updater(lambda mob: mob.next_to(probe, UP)),
                    Arrow(LEFT, RIGHT, stroke_color=YELLOW)
                    .add_updater(lambda mob: (mob.put_start_and_end_on(
                        rq := probe.get_center(),
                        rq + 16 * normalize(vect := source.get_center() - probe.get_center()) / get_norm(vect) ** 2
                    )))
                    )

        probe0, tex0, force0 = build_probe()
        probe1, tex1, force1 = build_probe()
        probe2, tex2, force2 = build_probe()
        self.add(source, tex_s, force0, probe0, tex0)
        self.wait()
        path1 = Line(ORIGIN, (-3, 2, 0)).shift(probe0.get_center())
        path2 = CubicBezier(ORIGIN, np.array((0, 1, 0)),
                            np.array((-1.5, 2, 0)), np.array((-3, 2, 0))).shift(probe0.get_center())
        force0.set_opacity(0.4)
        probe0.set_opacity(0.4)
        tex0.set_opacity(0.4)
        self.add(path1, path2, force1, force2, tex1, tex2, probe1, probe2)
        self.play(ShowCreation(path1), ShowCreation(path2),
                  MoveAlongBezier(probe1, probe0.get_center() + (ORIGIN, (-3, 2, 0))),
                  MoveAlongBezier(probe2, probe0.get_center() + (ORIGIN, (0, 1, 0), (-1.5, 2, 0), (-3, 2, 0))),
                  run_time=2)
        self.wait()
        self.play(Write(w1 := Tex(R"W").next_to(path1, DL, aligned_edge=UR, buff=0.1)),
                  Write(w2 := Tex(R"W").next_to(path2, UR, aligned_edge=DL, buff=0.5)))
        self.remove(probe2, tex2, force2)
        self.wait()

        self.play(ReplacementTransform(source, source := Charge(source.get_center(), 16, 0.4)),
                  ReplacementTransform(probe0, probe0 := Charge(probe0.get_center(), -1, 0.2).set_opacity(0.4)),
                  ReplacementTransform(probe1, probe1 := Charge(probe1.get_center(), -1, 0.2)),
                  Transform(tex_s, Tex(R"q_0").add_updater(lambda mob: mob.next_to(source, UP))),
                  Transform(tex0, Tex(R"q").add_updater(lambda mob: mob.next_to(probe0, UP)).set_opacity(0.4)),
                  Transform(tex1, Tex(R"q").add_updater(lambda mob: mob.next_to(probe1, UP))))
        self.wait()
        q = ValueTracker(1)
        zero = Dot((4, 0, 0))
        zero_tex = Tex(R"0").add_updater(lambda mob: mob.next_to(zero, DR))
        self.play(ReplacementTransform(tex1, DecimalNumber(
            source.get_phi(probe1.get_center()), num_decimal_places=2, unit="J"
        ).add_updater(
            lambda mob: mob.set_value(q.get_value() *
                                      (source.get_phi(probe1.get_center()) - source.get_phi(zero.get_center())))
        ).add_updater(
            lambda mob: mob.next_to(probe1, UP)
        )))
        self.wait()

        title = (Text("电势能", font_size=56)
                 .to_edge(UP))
        self.play(FadeIn(BackgroundRectangle(title)), Write(title),
                  *(FadeOut(mob) for mob in [probe0, force0, tex0, path1, path2, w1, w2]))
        self.wait()

        self.play(FocusOn(zero),
                  FadeIn(zero_tex, time_span=(1, 2)), GrowFromCenter(zero, time_span=(1, 2)))
        self.wait()
        # Now charge at (-1, 2, 0)
        self.remove(probe1, force1)
        self.add(Arrow(LEFT, RIGHT, stroke_color=YELLOW)
                 .add_updater(lambda mob: (mob.put_start_and_end_on(
                     rq := probe1.get_center(),
                     rq + 16 * normalize(vect := source.get_center() - probe1.get_center()) / get_norm(vect) ** 2
                 ))))
        self.add(path := CubicBezier(np.array((-1, 2, 0)), np.array((1.5, 2, 0)),
                                     np.array((4, 1, 0)), np.array((4, 0, 0))), probe1)
        self.play(ShowCreation(path),
                  MoveAlongBezier(probe1,
                                  ((-1, 2, 0), (1.5, 2, 0), (4, 1, 0), (4, 0, 0))),
                  run_time=3)
        self.wait()

        self.play(FadeOut(path),
                  MoveAlongBezier(probe1,
                                  ((4, 0, 0), (-1, 2, 0))))
        self.wait()
        self.play(probe1.animate.set_radius(0.4), q.animate.set_value(4), run_time=0.5)
        self.play(probe1.animate.set_radius(0.2), q.animate.set_value(1), run_time=0.5)
        self.wait()

        # Blackboard 分屏
        if DEBUG:
            self.add(Rectangle(FRAME_WIDTH/2, FRAME_HEIGHT))  # 答题卡裁切线 (bushi
        self.play(source.animate.move_to((-1, 0, 0)), probe1.animate.move_to((1, 2, 0)),
                  zero.animate.move_to((6, 0, 0)))
        self.wait()
        self.play(Transform(title, Text("电势", weight=BOLD, font_size=56)
                            .to_edge(UP)
                            .fix_in_frame()))
        self.wait()

        def phi_update(color: bool):
            last_zero = 0

            def updater(mob):
                nonlocal last_zero
                mob.shift((0, 0, last_zero - (new_zero := source.get_phi(zero.get_center()))))
                if color and last_zero != new_zero:
                    mob.set_color_by_rgb_func(color_by_z((BLUE, RED), -3, 3), opacity=0.8)
                last_zero = new_zero
            return updater

        # 3D 场景
        phi = (ParametricSurface(
            lambda u, v: (u, v, source.get_phi((u, v, 0))),
            (-FRAME_X_RADIUS*3, FRAME_X_RADIUS*3),
            (-FRAME_Y_RADIUS*3, FRAME_Y_RADIUS*3)
        ).set_shading(0, 0, 0))
        mesh = SurfaceMesh(phi)
        p1, p2, p3, p4 = (1, 2), (3, 3), (5, 4), (4.4, 3.7)
        p1p, p2p = source.get_phi((*p1, 0)), source.get_phi((*p2, 0))
        line_up = Line((*p1, p1p), (*p3, p1p), color=YELLOW)
        line_down = Line((*p2, p2p), (*p3, p2p), color=YELLOW)
        arrow_up = FillArrow((*p4, (p1p + p2p) / 2 + 0.3), (*p4, p1p), buff=0).set_color(YELLOW)
        arrow_down = FillArrow((*p4, (p1p + p2p) / 2 - 0.3), (*p4, p2p), buff=0).set_color(YELLOW)
        u_sign = (Tex(R"U", color=YELLOW)
                  .move_to((*p4, (p1p + p2p) / 2))
                  .rotate(PI/3, RIGHT)
                  .rotate(PI/4, OUT))
        phi.add_updater(phi_update(True))
        for mob in [mesh, line_up, line_down, arrow_up, arrow_down, u_sign]:
            mob.add_updater(phi_update(False))

        self.remove(zero, zero_tex, title)
        self.add(phi, mesh,
                 zero := Ball((6, 0, 0), 0.08, color=WHITE), zero_tex, title)
        self.play(
            fade_update(phi, 0.8, suspend_mobject_updating=True),
            stroke_fade_update(mesh, 0.8, suspend_mobject_updating=True),
            camera_update(self, [], [(PI/3, RIGHT, rush_from), (PI/4, OUT)], 2),
            run_time=2
        )
        self.wait()
        self.play(zero.animate.move_to((1, 2, 0)))
        self.play(zero.animate.move_to((3, 4, 0)),
                  *(Write(mob, suspend_mobject_updating=False)
                    for mob in [line_up, line_down, arrow_up, arrow_down, u_sign]))
        self.play(zero.animate.move_to((6, 0, 0)))
        self.play(zero.animate.move_to((514, 0, 0)))
        self.wait()

        axes = Axes((-24, 24, 1), (-12, 12, 1))
        field = VectorField(lambda x, y: (0, 0), axes)
        self.add(field)
        self.play(field.animate.become(VectorField(lambda x, y: source.get_e(axes.c2p(x, y)), axes)))
        self.wait()


class PotentialFormula(Scene):
    """tested with commit 259640f5 in osMrPigHead/manimgl
    新版公式渲染不正常"""
    def construct(self) -> None:
        coulombs_law = Tex(
            R"\vec{F} = {1 \over 4 \pi \varepsilon_0} {q_0 q \over r^2} \vec{e}_{r}"
        ).move_to((-3, -2, 0))
        coulombs_law_back = SurroundingRectangle(coulombs_law).set_fill(YELLOW, 0.2)
        gravity_law = Tex(
            R"\vec{F} = G {M m \over r^2} \vec{e}_{r}"
        ).move_to((3, -2, 0))
        gravity_law_back = SurroundingRectangle(gravity_law).set_fill(YELLOW, 0.2)
        self.play(ShowCreation(coulombs_law_back), Write(coulombs_law),
                  ShowCreation(gravity_law_back), Write(gravity_law), run_time=1.5)
        self.wait()
        e_p0 = round((source := Charge((-3, 0, 0), 16)).get_phi((-1, 2, 0)) - source.get_phi((4, 0, 0)), 2)
        self.play(Write(w := Tex(f"W=E_{{p0}}={e_p0}J").next_to(
            CubicBezier(np.array((-1, 2, 0)), np.array((1.5, 2, 0)),
                        np.array((4, 1, 0)), np.array((4, 0, 0))),
            UR, aligned_edge=DL, buff=0.75
        )))
        self.wait()
        self.play(*(FadeOut(mob) for mob in [coulombs_law, coulombs_law_back, gravity_law, gravity_law_back, w]))


class ConductionCurrent(Scene):
    """tested with commit 656f98fd in osMrPigHead/manimgl"""
    def construct(self) -> None:
        conduction_line = Cylinder(height=8, radius=0.15, color=GREY_D).rotate(PI/2, UP)
        self.add(conduction_line)
        self.wait()

        left = Line((-4, 0, 0), (-4, 2, 0), color=YELLOW)
        right = Line((4, 0, 0), (4, 2, 0), color=YELLOW)
        left_arrow = Arrow((-0.65, 1.5, 0), (-4, 1.5, 0), stroke_color=YELLOW, buff=0)
        right_arrow = Arrow((0.65, 1.5, 0), (4, 1.5, 0), stroke_color=YELLOW, buff=0)
        u_tex = Tex(R"U", color=YELLOW).move_to((0, 1.5, 0))
        self.remove(conduction_line)
        self.add(left, right, left_arrow, right_arrow, u_tex, conduction_line)
        self.play(*(Write(mob) for mob in [left, right, left_arrow, right_arrow, u_tex]))
        self.wait()
        electrons = Group(*(Electron((x, 0, 1)) for x in np.arange(-40, 10, 0.5)))
        self.play(UpdateFromAlphaFunc(electrons, lambda mob, alpha: (
            mob.set_opacity(alpha),
            mob.shift((2*alpha/DEFAULT_FPS, 0, 0)),
            None
        )[-1]))
        electrons.add_updater(lambda mob, dt: mob.shift((2*dt, 0, 0)))
        self.wait(4)
        e_arrow = FillArrow((1, 0, 0), (-1, 0, 0), buff=0).set_color(GREEN)
        e_tex = Tex(R"E", color=GREEN).next_to(e_arrow, UP)
        self.remove(electrons)
        self.add(e_arrow, electrons)
        self.play(Write(e_arrow), Write(e_tex))
        self.wait(1.5)

        force = Arrow((-0.2, 0, 0), (0.6, 0, 0), stroke_color=YELLOW, buff=0)
        electrons.clear_updaters(False)
        self.remove(electrons)
        self.add(e_arrow, force, electrons)
        self.play(camera_update(self, [], [], 0.2),
                  UpdateFromAlphaFunc(electrons, lambda mob, alpha: mob.shift((2*(1-alpha)/DEFAULT_FPS, 0, 0))),
                  Write(force), FadeOut(e_arrow), FadeOut(e_tex))
        self.wait(2)
        current = Arrow((0.4, 0.4, 0), (-0.4, 0.4, 0), stroke_color=BLUE, buff=0)
        current_tex = Tex(R"I", color=BLUE).scale(0.25).next_to(current, UP, buff=0.04)
        self.play(Write(current), Write(current_tex))
        self.wait()

        # Blackboard 分屏
        if DEBUG:
            self.add(Rectangle(FRAME_WIDTH/2, FRAME_HEIGHT))  # 答题卡裁切线 (bushi

        self.play(camera_update(self, [], [], 1, 0.2),
                  UpdateFromAlphaFunc(electrons, lambda mob, alpha: mob.shift((2*alpha/DEFAULT_FPS, 0, 0))),
                  *(FadeOut(mob) for mob in [force, current, current_tex]))
        electrons.add_updater(lambda mob, dt: mob.shift((2*dt, 0, 0)))
        self.wait()

        b_arrows = [
            FillArrow((-1.5, -0.35, 0.5+2**0.5/2), (-1.5, 0.35, 0.5+2**0.5/2),
                      buff=0)
            .rotate(PI/4*n, axis=LEFT, about_point=(-1.5, 0, 0)).set_color(BLUE) for n in range(8)
        ]
        self.play(*(FadeIn(b_arrow, time_span=(t_ * 0.1, t_ * 0.1 + 0.8))
                    for b_arrow, t_ in zip(b_arrows, range(8))),
                  Write(Tex(R"B", color=BLUE_D).next_to(b_arrows[1], LEFT)))
        self.wait()
        self.play(MoveAlongBezier(Charge((0, 0, 0), 1, 0.1, 0), [
            coord(-1, -1/8), coord(1/2, -1/8), coord(1, -1)
        ], time_span=(0, 0.7)), MoveAlongBezier(Charge((0, 0, 0), -1, 0.1, 0), [
            coord(-1, -1/2), coord(1/2, -1/2), coord(1, 0)
        ], time_span=(0.4, 1.1)), MoveAlongBezier(Charge((0, 0, 0), -1, 0.1, 0), [
            coord(-1, -3/4), coord(1/2, -3/4), coord(1, -1/8)
        ], time_span=(0.8, 1.5)), MoveAlongBezier(Charge((0, 0, 0), 1, 0.1, 0), [
            coord(-1, -1/4), coord(1/2, -1/4), coord(1, -1)
        ], time_span=(1.2, 1.9)))
        self.wait()


class MovingChargeAsCurrent(Scene):
    """tested with commit 656f98fd in osMrPigHead/manimgl"""
    def construct(self) -> None:
        def updater(mob: Charge, dt: float):
            nonlocal updater_time
            mob.shift((0, (math.sin(updater_time) -
                           math.sin(updater_time := updater_time + dt))/4, 0))
        animate_time = 1
        updater_time = animate_time
        q = Charge((-FRAME_X_RADIUS, 0, 0), 1, 0.6, 96).add_updater(updater)
        velocity = (Arrow(LEFT, RIGHT, stroke_color=BLUE)
                    .add_updater(lambda mob: mob.put_start_and_end_on(q.pos, q.pos + (2, 0, 0))))
        v_tex = (Tex(R"v", color=BLUE)
                 .add_updater(lambda mob: mob.next_to(velocity, UP)))
        current = Arrow((-1, 1.5, 0), (1, 1.5, 0), stroke_color=YELLOW)
        i_tex = Tex(R"I", color=YELLOW).next_to(current, UP)
        asl = AnimatedStreamLines(StreamLines(lambda x, y: (x-2, 0) if x <= 2 and -2 <= y <= 2
                                              else (0, 0), Axes()))
        self.add(asl, velocity, v_tex, q)
        self.play(UpdateFromAlphaFunc(
            q, lambda mob, alpha: (mob.move_to((
                (smooth(alpha)-1)*FRAME_X_RADIUS,
                -math.sin(alpha*animate_time)/4,
                0
            )), mob.set_opacity(smooth(alpha)), None)[-1],
            run_time=animate_time, rate_func=linear, suspend_mobject_updating=True),
                  FadeIn(velocity, suspend_mobject_updating=False),
                  FadeIn(v_tex, suspend_mobject_updating=False))
        self.wait(2)
        self.play(Write(current), Write(i_tex))
        self.wait(2)
        self.play(UpdateFromAlphaFunc(
            q, lambda mob, alpha: (mob.move_to((
                smooth(alpha)*FRAME_X_RADIUS,
                -math.sin(updater_time+alpha*animate_time)/4,
                0
            )), mob.set_opacity(1-smooth(alpha)), None)[-1],
            run_time=animate_time, rate_func=linear, suspend_mobject_updating=True),
                  fade_update(asl, 0, src_opacity=1),
                  FadeOut(i_tex), FadeOut(current),
                  FadeOut(velocity, suspend_mobject_updating=False),
                  FadeOut(v_tex, suspend_mobject_updating=False))


class InductionLines(Scene):
    """tested with commit 656f98fd in osMrPigHead/manimgl"""
    def construct(self) -> None:
        axes = Axes()
        asl = AnimatedStreamLines(StreamLines(u_bar_magnet_b, axes))
        bar_magnet = BarMagnet()
        self.add(asl, bar_magnet)
        self.play(FadeIn(bar_magnet))
        self.wait(2)
        start = axes.c2p(3/2, 1)
        b = axes.c2p(*u_bar_magnet_b(3/2, 1)) / 2
        gradient = color_gradient([RED, BLUE], 32)
        b_arrow = (Arrow(start, start + b)
                   .set_color_by_rgb_func(
                       lambda p: gradient[int(get_norm(p - start) / get_norm(b) * 32)].get_rgb()
                   ))
        self.play(Write(b_arrow))
        arrow_n_text = (Text("N", font_size=32, color=RED)
                        .next_to(b_arrow, UR, buff=0.1)
                        .shift((0, -b[1], 0)))
        arrow_s_text = (Text("S", font_size=32, color=BLUE)
                        .next_to(b_arrow, UL, buff=0.1))
        self.play(Write(arrow_n_text))
        self.play(Write(arrow_s_text))
        self.wait()
        rect = (Rectangle(1.5, 1, color=YELLOW)
                .move_to((-1.5, 1.25, 0)))
        self.play(ShowCreation(rect))
        self.wait()
        self.play(Transform(rect, Rectangle(1.5, 4, color=YELLOW)
                            .move_to((-5, 0, 0))))
        self.wait()
        self.play(FadeOut(rect))
        self.wait()
        field = VectorField(u_bar_magnet_b, axes).set_opacity(0.6)
        title = (Text("磁感应强度", font_size=56)
                 .to_edge(UP))
        b_tex = Tex(R"\vec{B}", color=BLUE).move_to((0, -3, 0))
        self.remove(bar_magnet, b_arrow, arrow_n_text, arrow_s_text)
        self.add(field, bar_magnet, b_arrow, arrow_n_text, arrow_s_text)
        self.play(Transform(asl, field), ShowCreation(field),
                  FadeIn(BackgroundRectangle(title), time_span=(1, 2)),
                  Write(title, time_span=(1, 2)),
                  FadeIn(BackgroundRectangle(b_tex), time_span=(1, 2)),
                  Write(b_tex, time_span=(1, 2)),
                  run_time=2)
        self.wait()
        b_unit = (TexText(R"T\;(特斯拉)", font_size=36, color=YELLOW)
                  .next_to(b_tex, UR, buff=0.1))
        self.play(FadeIn(BackgroundRectangle(b_unit)), Write(b_unit))
        self.wait()


class UniformMagnetField(Scene):
    """tested with commit 259640f5 in osMrPigHead/manimgl"""
    def construct(self) -> None:
        magnet_n = (Rectangle(2, FRAME_HEIGHT)
                    .set_fill(RED, 1)
                    .set_stroke(RED, 0))
        magnet_n.add(Text("N", font_size=64, color=RED_E))
        magnet_n.to_edge(LEFT, buff=0)
        magnet_s = (Rectangle(2, FRAME_HEIGHT)
                    .set_fill(BLUE_D, 1)
                    .set_stroke(BLUE_D, 0))
        magnet_s.add(Text("S", font_size=64, color=BLUE_E))
        magnet_s.to_edge(RIGHT, buff=0)
        axes = Axes()
        field = VectorField(lambda x, y: (0, 0), axes)
        self.add(field, magnet_n, magnet_s,
                 AnimatedStreamLines(StreamLines(lambda x, y: (1.5, 0.), axes)))
        self.wait()
        title = (Text("匀强磁场", font_size=56)
                 .to_edge(UP))
        self.play(field.animate.become(VectorField(lambda x, y: (1., 0.), axes)),
                  FadeIn(BackgroundRectangle(title)),
                  Write(title))
        self.wait()


class BarMagnetField(Scene):
    """tested with commit 656f98fd in osMrPigHead/manimgl"""
    def construct(self) -> None:
        axes = Axes()
        bar_magnet = BarMagnet()
        field = VectorField(lambda x, y: (0, 0), axes)
        self.add(field, bar_magnet)
        self.wait()
        self.play(field.animate.become(VectorField(u_bar_magnet_b, axes)))
        self.wait()


class BarMagnetForce(Scene):
    """tested with commit 656f98fd in osMrPigHead/manimgl"""
    def construct(self) -> None:
        d = 11/4
        m1 = BarMagnet().scale(0.6).next_to((-d, 0, 0), LEFT, buff=0)
        m2 = BarMagnet().scale(0.6).next_to((d, 0, 0), RIGHT, buff=0)
        self.add(m1, m2)
        self.play(UpdateFromAlphaFunc(
            m1,
            lambda mob, alpha: mob.next_to((-d+d*rush_into(alpha), 0, 0), LEFT, buff=0)
        ), UpdateFromAlphaFunc(
            m2,
            lambda mob, alpha: mob.next_to((d-d*rush_into(alpha), 0, 0), RIGHT, buff=0)
        ))
        self.wait()
        force_arrow = Arrow((0, 0, 0), (7/4, 0, 0), stroke_color=YELLOW, buff=0)
        force_tex = Tex(R"F", color=YELLOW).next_to(force_arrow, UP)
        self.play(m2.animate.set_opacity(0.6),
                  FadeIn(force_arrow), FadeIn(force_tex))
        self.wait()
        self.play(ShowCreationThenFadeOut(Rectangle(1, 1.5, color=YELLOW)
                                          .move_to(m1)))
        self.wait()
        cbu = cubic_bezier(
            (2/3, 0, 0), (2/9, 1/3, 0), (-2/9, 1/3, 0), (-2/3, 0, 0)
        ).shift(m1.get_top()).set_stroke(BLUE)
        cbd = cubic_bezier(
            (2/3, 0, 0), (2/9, -1/3, 0), (-2/9, -1/3, 0), (-2/3, 0, 0)
        ).shift(m1.get_bottom()).set_stroke(BLUE)
        self.play(ShowCreation(cbu), ShowCreation(cbd), run_time=0.6)
        self.wait()


class UniformWorksForElectric(Scene):
    """tested with commit 656f98fd in osMrPigHead/manimgl"""
    def construct(self) -> None:
        r = 3
        q = TrueDot(color=RED, radius=r+1/4).make_3d()
        pppppp114514 = VGroup(*(Text("+", font_size=20, color=BLACK)
                                .move_to((r*math.cos(t), r*math.sin(t), 0))
                                for t in np.arange(0, 2*PI, PI/16)))
        self.add(q, pppppp114514)


class ButNotForMagnet(Scene):
    """tested with commit 656f98fd in osMrPigHead/manimgl"""
    def construct(self) -> None:
        r = 3
        m = TrueDot(color=BLUE_D, radius=r+1/4).make_3d()
        n_text = Text("S", font_size=192, color=BLUE_E)
        self.add(m, n_text)


class BigQuestionMark(big_question_mark.BigQuestionMark):
    """tested with commit 259640f5 in osMrPigHead/manimgl"""
    pass


class LorentzForce(Scene):
    """tested with commit 656f98fd in osMrPigHead/manimgl"""
    def construct(self) -> None:
        def updater(mob: Charge, dt: float):
            nonlocal updater_time
            mob.shift((0, (math.sin(updater_time) -
                           math.sin(updater_time := updater_time + dt))/4, 0))
        animate_time = 1
        updater_time = animate_time
        q = Charge((-FRAME_X_RADIUS, 0, 0), 1, 0.6, 96).add_updater(updater)
        velocity = (Arrow(LEFT, RIGHT, stroke_color=BLUE)
                    .add_updater(lambda mob: mob.put_start_and_end_on(q.pos, q.pos + (2, 0, 0))))
        v_tex = (Tex(R"v", color=BLUE)
                 .add_updater(lambda mob: mob.next_to(velocity, UP)))
        asl = AnimatedStreamLines(StreamLines(lambda x, y: (x-2, 0) if x <= 2 and -2 <= y <= 2
                                              else (0, 0), Axes()))
        xxxxxx114514 = (VGroup(*(Text("+", font_size=20, color=BLUE_D)
                                 .rotate(PI/4)
                                 .move_to((x, y + 0.5, 0))
                                 for x in range(-8, 40) for y in range(-5, 5)))
                        .add_updater(lambda mob, dt: mob.shift((-dt/2, 0, 0)))
                        .set_opacity(0))
        self.add(asl, xxxxxx114514, velocity, v_tex, q)
        self.play(UpdateFromAlphaFunc(
            q, lambda mob, alpha: (mob.move_to((
                (smooth(alpha)-1)*FRAME_X_RADIUS,
                -math.sin(alpha*animate_time)/4,
                0
            )), mob.set_opacity(smooth(alpha)), None)[-1],
            run_time=animate_time, rate_func=linear, suspend_mobject_updating=True),
                  FadeIn(velocity, suspend_mobject_updating=False),
                  FadeIn(v_tex, suspend_mobject_updating=False))
        self.wait()
        velocity.clear_updaters()
        self.play(q.animate.scale(0.5), xxxxxx114514.animate.set_opacity(1),
                  UpdateFromAlphaFunc(velocity, lambda mob, alpha:
                  mob.put_start_and_end_on(q.pos, q.pos + (2 - alpha, 0, 0))))
        velocity.add_updater(lambda mob: mob.put_start_and_end_on(q.pos, q.pos + (1, 0, 0)))
        self.wait()
        force_arrow = (Arrow(LEFT, RIGHT, stroke_color=YELLOW)
                       .add_updater(lambda mob: mob.put_start_and_end_on(
                           q.get_center(), q.get_center() + (0, 1.5, 0)
                       )))
        force_tex = (Tex(R"F", color=YELLOW)
                     .add_updater(lambda mob: mob.next_to(force_arrow, LEFT)))
        self.remove(q)
        self.add(force_arrow, force_tex, q)
        self.play(Write(force_arrow), Write(force_tex))
        self.wait()
        self.play(FocusOn(q, suspend_mobject_updating=False))
        self.wait()
        self.play(Indicate(velocity, suspend_mobject_updating=False),
                  Indicate(v_tex, suspend_mobject_updating=False))
        self.wait()


class LorentzForceFormula(Scene):
    """tested with commit 259640f5 in osMrPigHead/manimgl"""
    def construct(self) -> None:
        title = (Text("洛伦兹力", font_size=56)
                 .to_edge(UP))
        lorentz_force = Tex(
            R"\vec{F} = q \vec{v} \times \vec{B}"
        ).to_edge(DOWN, buff=1)
        lorentz_force_back = SurroundingRectangle(lorentz_force).set_fill(YELLOW, 0.2)
        self.play(FadeIn(BackgroundRectangle(title)), Write(title),
                  ShowCreation(lorentz_force_back), Write(lorentz_force))
        self.wait()
        lorentz_force_back_ = (SurroundingRectangle(lorentz_force.generate_target()
                                                    .scale(1.5).move_to((0, 0, 0)))
                               .set_fill(YELLOW, 0.2)
                               .set_opacity(0))
        self.play(MoveToTarget(lorentz_force),
                  Transform(lorentz_force_back, lorentz_force_back_))
        self.wait()
        focus = SurroundingRectangle(lorentz_force[R"q \vec{v}"])
        self.play(ShowCreation(focus))
        self.wait()
        focus_ = SurroundingRectangle(lorentz_force[R"\vec{B}"])
        self.play(Transform(focus, focus_))
        self.wait()
        b_unit = Tex(
            R"N = C \cdot ( m / s ) \cdot T", color=YELLOW
        ).next_to(lorentz_force, DOWN, buff=0.6)
        self.play(Write(b_unit))
        self.wait()
        b_unit_ = Tex(
            R"T = N \cdot s / ( C \cdot m )", color=YELLOW
        ).next_to(lorentz_force, DOWN, buff=0.6)
        self.play(TransformMatchingTex(b_unit, b_unit_, key_map={
            "N": "N",
            "C": "C",
            "m": "m",
            "s": "s",
            "T": "T"
        }, path_arc=True))
        self.wait()
        focus_ = SurroundingRectangle(lorentz_force[R"\times"])
        self.play(Transform(focus, focus_))
        self.wait()
        cross_image = (ImageMobject("optics/cross.png", 4)
                       .next_to(lorentz_force, LEFT))
        self.play(FadeIn(cross_image))
        self.wait()
        # self.add(MotionMobject(Dot().set_color(MAROON))
        #          .add_updater(lambda mob: print(mob.get_center())))
        # 食指: [-5.55 0.04] -- [-3.94 -0.54]
        # 中指: [-5.22 -1.22] -- [-4.27 -0.61]
        # 大拇指: [-3.86 0.87] -- [-3.23 -0.17]
        rect = rect_from_to((-5.55, 0.04), (-3.94, -0.54), color=YELLOW)
        self.play(ShowCreation(rect))
        self.wait()
        self.play(Transform(rect, rect_from_to((-5.22, -1.22), (-4.27, -0.61),
                                               color=YELLOW)))
        self.wait()
        self.play(Transform(rect, rect_from_to((-3.86, 0.87), (-3.23, -0.17),
                                               color=YELLOW)))
        self.wait()
        self.play(FadeOut(rect))
        self.wait()
        cross_image.add_updater(lambda mob, dt: mob.rotate(4*PI*dt))
        self.wait()
        cross_image.clear_updaters()
        self.wait()
        lorentz_force_abs = Tex(
            R"|\vec{F}| = q |\vec{v}||\vec{B}| \sin\theta"
        ).next_to(b_unit, DOWN, buff=0.6)
        self.play(Write(lorentz_force_abs))
        self.wait()


DEBUG = False


class Blackboard(Scene):
    """tested with commit 259640f5 in osMrPigHead/manimgl"""
    SPLIT = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.coulombs_law_title = (Text("库仑定律:", font_size=36)
                                   .to_edge(UL, buff=0.5))
        self.coulombs_law = Tex(
            R"\vec{F} = {1 \over 4 \pi \varepsilon_0} {q_0 q \over r^2} \vec{e}_{r}"
        ).scale(0.75).next_to(self.coulombs_law_title, RIGHT, aligned_edge=LEFT, buff=1)

        self.e_field_intensity_title = (Text("电场强度:", font_size=36)
                                        .next_to(self.coulombs_law_title, DOWN, aligned_edge=UL, buff=0.8))
        self.e_field_intensity = Tex(
            R"\vec{E} = {\vec{F} \over q} = {1 \over 4 \pi \varepsilon_0} {q_0 \over r^2} \vec{e}_{r}"
        ).scale(0.75).next_to(self.e_field_intensity_title, RIGHT, aligned_edge=LEFT, buff=1)
        self.e_field_intensity_unit_1 = TexText(
            R"\small N/C\;(牛每库)", color=YELLOW
        ).scale(0.75).next_to(self.e_field_intensity, DOWN, aligned_edge=UP, buff=0.6)
        self.e_field_intensity_unit_2 = TexText(
            R"\small V/m\;(伏每米)", color=YELLOW
        ).scale(0.75).next_to(self.e_field_intensity, DOWN, aligned_edge=UP, buff=0.6)
        self.f_qe = Tex(
            R"\vec{F} = q \vec{E}"
        ).scale(0.75).next_to(self.e_field_intensity_title, DOWN, aligned_edge=UL, buff=0.6)

        self.phi_title = (Text("电势:", font_size=36)
                          .next_to(self.f_qe, DOWN, aligned_edge=UL, buff=0.8))
        self.phi = Tex(
            R"\varphi = {E_p \over q}"
        ).scale(0.75).next_to(self.phi_title, RIGHT, aligned_edge=LEFT, buff=0.65)
        self.phi_unit_1 = TexText(
            R"\small J/C\;(焦每库)", color=YELLOW
        ).scale(0.75).next_to(self.phi, DOWN, aligned_edge=UP, buff=0.6)
        self.phi_unit_2 = TexText(
            R"\small V\;(伏特)", color=YELLOW
        ).scale(0.75).next_to(self.phi, DOWN, aligned_edge=UP, buff=0.6)

        self.i_title = (Text("传导电流:", font_size=36)
                        .next_to(self.phi_title, DOWN, aligned_edge=UL, buff=0.8))
        self.i = Tex(
            R"I = {\Delta q \over \Delta t}"
        ).scale(0.75).next_to(self.i_title, RIGHT, aligned_edge=LEFT, buff=1)
        self.i_unit_1 = TexText(
            R"\small C/s\;(库每秒)", color=YELLOW
        ).scale(0.75).next_to(self.i, DOWN, aligned_edge=UP, buff=0.6)
        self.i_unit_2 = TexText(
            R"\small A\;(安培)", color=YELLOW
        ).scale(0.75).next_to(self.i, DOWN, aligned_edge=UP, buff=0.6)

    def construct(self) -> None:
        if DEBUG and self.SPLIT:
            match self.SPLIT:  # 答题卡裁切线 (bushi
                case 1: self.add(Rectangle(FRAME_WIDTH/2, FRAME_HEIGHT).to_edge(LEFT, buff=0))
                case 2: self.add(Rectangle(FRAME_WIDTH/2, FRAME_HEIGHT).to_edge(RIGHT, buff=0))
        # self.e_field()
        # self.potential()
        self.conduction_current()

    def e_field(self) -> None:
        self.add(self.coulombs_law_title, self.coulombs_law)
        self.wait()

        self.play(ShowCreationThenFadeAround(self.coulombs_law[R"q"]))
        self.wait()

        self.play(Write(self.e_field_intensity_title))
        self.play(Write(self.e_field_intensity[R"\vec{E} = {\vec{F} \over q}"]))
        self.wait()
        self.play(Write(self.e_field_intensity_unit_1))
        self.wait()
        self.play(TransformFromCopy(
            self.coulombs_law[R"= {1 \over 4 \pi \varepsilon_0} {q_0 q \over r^2} \vec{e}_{r}"],
            self.e_field_intensity[R"= {1 \over 4 \pi \varepsilon_0} {q_0 \over r^2} \vec{e}_{r}"],
            path_arc=2,
            path_arc_axis=IN,
            run_time=2
        ))
        self.wait()
        self.play(Write(self.f_qe))
        self.wait()

    def potential(self) -> None:
        self.add(self.coulombs_law_title, self.coulombs_law,
                 self.e_field_intensity_title, self.e_field_intensity, self.f_qe)
        self.wait()

        self.play(ShowCreationThenFadeAround(self.f_qe[R"q"]))
        self.wait()
        self.play(Write(w := Tex(R"W = \vec{F} \cdot \Delta\vec{r}", color=BLUE).scale(0.75)
                        .next_to(self.f_qe, RIGHT, aligned_edge=LEFT, buff=2)
                        .shift((0.5, -0.5, 0))))
        self.wait()
        self.play(Write(Tex(R"E_p \propto q", color=BLUE).scale(0.75)
                        .next_to(w, DOWN, aligned_edge=UP, buff=0.5)))
        self.wait()

        self.play(Write(self.phi_title))
        self.play(Write(self.phi))
        self.wait()
        self.play(Write(self.phi_unit_1))
        self.wait()
        self.play(Transform(self.phi_unit_1, self.phi_unit_2))
        self.wait()

    def conduction_current(self) -> None:
        self.add(self.coulombs_law_title, self.coulombs_law,
                 self.e_field_intensity_title, self.e_field_intensity, self.e_field_intensity_unit_1, self.f_qe,
                 self.phi_title, self.phi)
        self.wait()
        self.play(Transform(self.e_field_intensity_unit_1, self.e_field_intensity_unit_2))
        self.wait()
        self.play(Write(self.i_title))
        self.play(Write(self.i))
        self.wait()
        self.play(Write(self.i_unit_1))
        self.wait()
        self.play(Transform(self.i_unit_1, self.i_unit_2))
        self.wait()
