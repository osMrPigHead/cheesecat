"""常用场景"""
from manimlib import *


class TocParent(Scene):
    """tested with commit 259640f5 in osMrPigHead/manimgl"""
    p_shift = np.array((0, 0.4, 0))
    title_p_buff = 1
    p_buff = 0.8
    p_edge_buff = 1

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.title = TexText(R"\large 目\,录").to_edge(UP, buff=0.4).fix_in_frame()
        self.underline = Underline(self.title)
        self.underline.set_width(self.underline.get_width() + 0.75).fix_in_frame()
        self.p1 = (TexText(R"基础知识",
                           alignment=R"\raggedright")
                   .next_to(self.underline, DOWN, aligned_edge=UP, buff=self.title_p_buff)
                   .to_edge(LEFT, buff=self.p_edge_buff)
                   .fix_in_frame())
        self.p2 = (TexText(R"光的本质\\\footnotesize 电磁波是什么？如何产生、传播？和光速有什么关系？",
                           alignment=R"\raggedright")
                   .next_to(self.p1, DOWN, aligned_edge=UP, buff=self.p_buff)
                   .to_edge(LEFT, buff=self.p_edge_buff)
                   .fix_in_frame())
        self.p3 = (TexText(R"光的干涉与衍射\\\footnotesize 图样是怎么来的？干涉和衍射有什么关系？",
                           alignment=R"\raggedright")
                   .next_to(self.p2, DOWN, aligned_edge=UP, buff=self.p_buff)
                   .to_edge(LEFT, buff=self.p_edge_buff)
                   .fix_in_frame())
        self.p4 = (TexText(R"光的折射与反射\\\footnotesize 光折射和反射现象背后的本质是什么？折射和反射定律又是为什么？",
                           alignment=R"\raggedright")
                   .next_to(self.p3, DOWN, aligned_edge=UP, buff=self.p_buff)
                   .to_edge(LEFT, buff=self.p_edge_buff)
                   .fix_in_frame())

    def construct(self) -> None:
        self.add(self.title, self.underline, self.p1, self.p2, self.p3, self.p4)
