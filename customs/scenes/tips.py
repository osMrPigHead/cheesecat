"""温馨提示"""
from manimlib import *


class Tips(Scene):
    """tested with commit 88df1dca in osMrPigHead/manimgl"""
    title = "温馨提示"
    content = "你好世界!"
    max_width = FRAME_WIDTH - 3.5
    underline_width = max_width + 0.4
    title_font_size = 56
    title_buff = 1
    underline_buff = 0.2
    font_size = 42
    lsh = 1.2
    indent = 2.65
    content_buff = 0.4
    lag_ratio = 0.1
    run_time_per_char = 0.1

    def construct(self) -> None:
        self.title_mobject = (Title(self.title, font_size=self.title_font_size,
                                    underline_width=self.underline_width,
                                    color=YELLOW, underline_buff=self.underline_buff,
                                    underline_style={"stroke_color": YELLOW})
                              .to_edge(UP, buff=self.title_buff))
        self.add(self.title_mobject, self.title_mobject)
        self.content_mobject = (Text(self.content, font_size=self.font_size, lsh=self.lsh,
                                     indent=self.font_size * self.indent, line_width=self.max_width)
                                .next_to(self.title_mobject, DOWN, buff=self.content_buff))
        self.play(Write(self.content_mobject, run_time=self.run_time_per_char * len(self.content),
                        lag_ratio=self.lag_ratio))
        self.wait(2)
