"""开场名言"""
__all__ = [
    "OpeningQuote"
]

from manimlib import *


class OpeningQuote(Scene):
    """tested with commit 6d69b8fe in osMrPigHead/manimgl"""
    # (quote, author, is_chinese, highlights)
    quote_settings = [(R"你好 世界!", R"osMrPigHead", True, {"世界!": BLUE}),
                      (R"Hello world!", R"osMrPigHead", False, {"world!": BLUE})]
    use_quotation_marks = True
    max_width = FRAME_WIDTH - 1
    quote_buff = 1
    author_buff = 0.75
    lag_ratio = 0.1
    run_time_per_char = 0.07

    def construct(self) -> None:
        self.quotes, self.authors = self.get_quotes_and_authors()
        self.play(*(VFadeIn(quote, run_time=self.run_time_per_char * max(len(quote) for quote, _, _, _
                                                                         in self.quote_settings),
                            lag_ratio=self.lag_ratio) for quote in self.quotes))
        self.wait(2)
        self.play(*(Write(author, run_time=3) for author in self.authors))
        self.wait(2)

    def get_quotes_and_authors(self) -> tuple[list[TexText], list[TexText]]:
        quotes = []
        authors = []
        for quote, author, chinese, highlights in self.quote_settings:
            quotes += [TexText(*(r"``" + quote + "''")
                               .split(" ") if self.use_quotation_marks else quote,
                               tex_to_color_map=highlights)
                       .set_max_width(self.max_width)
                       .next_to(authors[-1] if authors else TOP, DOWN, buff=self.quote_buff)]
            authors += [TexText(r"\textemdash " * (2 if chinese else 1) + author)
                        .set_max_width(self.max_width)
                        .next_to(quotes[-1], DOWN, buff=self.author_buff)
                        .set_color(YELLOW)]
        return quotes, authors
