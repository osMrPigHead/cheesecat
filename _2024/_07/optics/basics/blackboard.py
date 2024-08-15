"""基础知识篇: 敲黑板划重点"""
from cc_config import *
from manimlib import *


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

        self.biot_savart_law_title = (Text("毕奥-萨伐尔定律:", font_size=36)
                                      .next_to(self.i_title, DOWN, aligned_edge=UL, buff=0.8))
        self.biot_savart_law = (Tex(
            R"\vec{B} = {\mu_0  \over 4 \pi } {q \vec{v} \times \vec{e}_r  \over r^2 }"
            R"        = {\mu_0 \over 4 \pi} {I \Delta \vec{l} \times \vec{e}_r \over r^2}"
        ).scale(0.75).next_to(self.biot_savart_law_title, RIGHT, aligned_edge=LEFT, buff=1.6))
        self.biot_savart_law_mu0 = (TexText(R"真空磁导率", color=YELLOW, font_size=36)
                                    .next_to(self.biot_savart_law[R"\mu_0  "], UP, aligned_edge=DL, buff=0.3))

        self.line_b_title = (Text("无限长通电直导线的磁场:", font_size=36)
                             .next_to(self.biot_savart_law_title, DOWN, aligned_edge=UL, buff=0.8))
        self.line_b_1 = (Tex(
            R"B = {\mu_0 I l \over 2 \pi r l}"
        ).scale(0.75).next_to(self.line_b_title, RIGHT, aligned_edge=LEFT, buff=2.2))
        self.line_b_2 = (Tex(
            R"B = {\mu_0 I \over 2 \pi r}"
        ).scale(0.75).next_to(self.line_b_title, RIGHT, aligned_edge=LEFT, buff=2.2))

    def construct(self) -> None:
        if DEBUG and self.SPLIT:
            match self.SPLIT:  # 答题卡裁切线 (bushi
                case 1: self.add(Rectangle(FRAME_WIDTH/2, FRAME_HEIGHT).to_edge(LEFT, buff=0))
                case 2: self.add(Rectangle(FRAME_WIDTH/2, FRAME_HEIGHT).to_edge(RIGHT, buff=0))
        # self.e_field()
        # self.potential()
        # self.conduction_current()
        self.biot_savart()

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

    def biot_savart(self) -> None:
        self.add(self.coulombs_law_title, self.coulombs_law,
                 self.e_field_intensity_title, self.e_field_intensity, self.f_qe,
                 self.phi_title, self.phi,
                 self.i_title, self.i)
        self.wait()
        self.play(Write(self.biot_savart_law_title))
        self.play(Write(self.biot_savart_law[
                            R"\vec{B} = {\mu_0  \over 4 \pi } {q \vec{v} \times \vec{e}_r  \over r^2 }"
                        ]))
        self.wait()
        self.play(ShowCreationThenFadeAround(self.biot_savart_law[R"\mu_0  "]))
        self.wait()
        self.play(Write(self.biot_savart_law_mu0))
        self.wait()
        self.play(ShowCreationThenFadeAround(self.biot_savart_law[R"\vec{e}_r  "]))
        self.wait()
        self.play(ShowCreationThenFadeAround(self.biot_savart_law[R"r^2 "]))
        self.wait()
        self.play(ShowCreationThenFadeAround(self.biot_savart_law[R"\vec{B}"]))
        self.wait()
        self.play(CircleIndicate(self.biot_savart_law[R"r^2 "]),
                  CircleIndicate(self.e_field_intensity[R"r^2"]))
        self.wait()
        self.play(CircleIndicate(self.biot_savart_law[R"q \vec{v}"]),
                  CircleIndicate(self.e_field_intensity[R"q_0"]))
        self.wait()
        self.play(TransformFromCopy(
            self.biot_savart_law[
                R"= {\mu_0  \over 4 \pi } {q \vec{v} \times \vec{e}_r  \over r^2 }"
            ], self.biot_savart_law[
                R"= {\mu_0 \over 4 \pi} {I \Delta \vec{l} \times \vec{e}_r \over r^2}"
            ],
            path_arc=2,
            run_time=2
        ))
        self.wait()
        fpi = self.biot_savart_law[R"4 \pi "]
        t, b, l, r = fpi.get_top(), fpi.get_bottom(), fpi.get_left(), self.biot_savart_law[R"r^2 "].get_right()
        rect = (Rectangle((r - l)[0] + 0.2, (t - b)[1] + 0.2)
                .move_to(((r+l)[0]/2, (t+b)[1]/2, 0))
                .set_stroke(YELLOW))
        self.play(ShowCreationThenFadeOut(rect))
        self.wait()
        self.play(Write(self.line_b_title))
        self.play(Write(self.line_b_1))
        self.wait()
        self.play(TransformMatchingTex(self.line_b_1, self.line_b_2, key_map={
            R"\mu_0 I": R"\mu_0 I",
            R"2 \pi r": R"2 \pi r",
            R"\over": R"\over"
        }, run_time=1))
        self.wait()
        self.play(ShowCreationThenFadeAround(self.coulombs_law[R"4 \pi \varepsilon_0"]))
        self.wait()
