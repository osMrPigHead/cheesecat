"""光的本质篇"""
from _2024._07.optics.scenes import *
from manimlib import *


class Toc(TocParent):
    """tested with commit a4210293 in osMrPigHead/manimgl"""
    def construct(self) -> None:
        super().construct()
        self.wait(1)
        self.play(ShowCreation(p2s := SurroundingRectangle(self.p2)))
        self.play(FadeOut(p2s),
                  self.p1.animate.set_color(GREY),
                  self.p3.animate.set_color(GREY),
                  self.p4.animate.set_color(GREY))
        self.wait(6)

