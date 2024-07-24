"""引入和目录部分"""
from typing import *

from _2024._07.optics.light import *
from _2024._07.optics.scenes import *
from customs.scenes import opening_quote, tips, toc
from customs.coords import *
from customs.utils import *
from manimlib import *


class OpeningQuote(opening_quote.OpeningQuote):
    """tested with commit 6d69b8fe in osMrPigHead/manimgl"""
    quote_settings = [
        (R"It is a universal condition of the enjoyable that the mind must believe in the existence of a law, and yet "
         R"have a mystery to move about in.", R"James C. Maxwell", False, {"mystery": BLUE}),
        (R"欢愉的普遍之道在于，相信真理的存在，而始终葆有神秘与好奇。", R"詹姆斯·麦克斯韦", True, {"神秘与好奇": BLUE})
    ]


class QuestionsGeometricalOptic(Scene):
    """tested with commit 6d69b8fe in osMrPigHead/manimgl"""
    def construct(self) -> None:
        self.add(glass := Rectangle(FRAME_WIDTH, 4/9*FRAME_HEIGHT,
                                    color=BLUE_E, fill_opacity=0.4, stroke_opacity=0)
                 .to_edge(DOWN, buff=0))

        anims = []
        time_last = 0
        for _ in range(4):
            anims += (anim := transmit_light_flash_(
                *light_from_path((fullrand(), 1), (fullrand(0.2), -1/9)),
                ((-1, -1/9), (1, -1/9)), 4/3, time_start=time_last
            ))[0]
            time_last = anim[1] + fullrand(0.4)
        self.play(*anims)
        self.wait(2)

        self.play((Rectangle(FRAME_WIDTH, 1e-4,
                             color=TEAL_E, fill_opacity=0.4, stroke_opacity=0)
                   .next_to(glass, UP, buff=0))
                  .animate.set_height(FRAME_HEIGHT/36, stretch=True, about_edge=DOWN),
                  ShowCreation(arrow := Arrow(coord(-3/4, 1/4), coord(-2/3, -1/12))),
                  Write(Text("增透膜")
                        .move_to(arrow.get_start() + coord(0, 1/18), DOWN)),
                  run_time=0.7)
        anims = []
        time_last = 0
        for _ in range(2):
            anims += (anim := transmit_light_flash_(
                p := (1/4 + fullrand(0.2), 1/2 + fullrand(0.2)), -1-1.3j+fullrand(0.1)+fullrand(0.1j),
                ((-1, -1/9), (1, -1/9)), reverse=True, time_start=time_last
            ))[0]
            anims += transmit_light_flash(
                p, -1-1.8j+fullrand(0.1)+fullrand(0.1j),
                ((-1, -1/18), (1, -1/18)), reverse=True, time_end=anim[1]
            )
            anims += [Flash(coord(p), run_time=anim[1] + 0.7,
                            time_span=(anim[1] - WIDTH_RATE, anim[1] - WIDTH_RATE + 0.7))]
            time_last = anim[1] - WIDTH_RATE + 0.7 + fullrand() * 0.4
        self.play(*anims)
        self.play(*list(zip(*transmit_light_path(
            (1/4, 1/2), -1-1.5j,
            ((-1, -1/9), (1, -1/9)), 4/3, reverse=True, reflect_dashed=True
        )))[0])
        self.wait(2)


class QuestionsPolarization(WavePropagation):
    """tested with commit 88df1dca in osMrPigHead/manimgl"""
    pass


class Tips(tips.Tips):
    """tested with commit 88df1dca in osMrPigHead/manimgl"""
    content = ("本视频内容大多不是高考所要求的，不推荐正在备考的观众观看。\n"
               "由于微积分不是高中课纲内容，本视频中数学推导均有适当简化。\n"
               "本视频出现的公式中，矢量用加粗字母标出，但表示矢量大小的字母不加粗。\n"
               "本视频由一名高中生制作，错误和不严谨之处在所难免，敬请指正。")


class Toc(toc.Toc):
    """tested with commit 88df1dca in osMrPigHead/manimgl"""
    # TODO: 中间过程播放相应视频
    toc = [
        (R"光的本质\\"
         R"\footnotesize 光是什么？电磁场的变化如何激发电磁波？电磁波如何在空间中传递？", lambda x: x.wait(4)),
        (R"光的干涉与衍射\\"
         R"\footnotesize 干涉图样何来？干涉与衍射有何联系？", lambda x: x.wait(4)),
        (R"光的折射与反射\\"
         R"\footnotesize 光为何``弯折''？光为何变慢？反射角与入射角为何恰巧相等？", lambda x: x.wait(4))
    ]
