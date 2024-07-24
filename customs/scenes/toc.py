"""目录"""
from manimlib import *


class Toc(Scene):
    """tested with commit 88df1dca in osMrPigHead/manimgl"""
    title = "目录"
    # (content, do_something(self))
    toc = [
        (R"Hello world!\\\footnotesize{你好世界!}", lambda x: None),
        (R"你好世界!\\\footnotesize{Hello world!}", lambda x: None)
    ]
    title_font_size = 56
    title_buff = 0.5
    underline_buff = 0.2
    toc_buff = 1
    toc_buff_between = 0.6
    shift_height = 0.2
    title_fade_time = 0.6
    toc_fade_time = 0.6

    def construct(self) -> None:
        self.title_mobject = (Title(self.title, font_size=self.title_font_size,
                                    underline_buff=self.underline_buff)
                              .to_edge(UP, buff=self.title_buff))
        self.play(VFadeIn(self.title_mobject, run_time=self.title_fade_time))
        self.toc_mobjects = self.get_toc_mobjects()
        for (_, func), toc_mobject in zip(self.toc, self.toc_mobjects):
            self.play(FadeIn(toc_mobject, shift=np.array((0, self.shift_height, 0)),
                             run_time=self.toc_fade_time))
            func(self)
        self.wait(2)


    def get_toc_mobjects(self) -> list[TexText]:
        res = []
        for content, _ in self.toc:
            res += [TexText(content, alignment=R"\raggedright")
                    .next_to(res[-1] if res else self.title_mobject, DOWN,
                             buff=self.toc_buff_between if res else self.toc_buff,
                             aligned_edge=LEFT)]
        return res
