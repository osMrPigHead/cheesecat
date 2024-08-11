"""小朋友你是否有很多问号"""
__all__ = [
    "BigQuestionMark"
]

from manimlib import *


class BigQuestionMark(Scene):
    """tested with commit 259640f5 in osMrPigHead/manimgl"""
    time_ = 3
    font_size = 576
    font_color = WHITE

    def construct(self) -> None:
        self.play(Write(Tex(R"?", font_size=self.font_size, color=WHITE)),
                  run_time=self.time_)
        self.wait()
