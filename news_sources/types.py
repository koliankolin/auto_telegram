from dataclasses import dataclass


@dataclass
class News:
    title: str
    summary: str
    img_url: str

    def __hash__(self):
        return hash(f"{self.title}{self.summary}")

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __ne__(self, other):
        return not self.__eq__(other)


@dataclass
class NYTimesNews(News):
    def __hash__(self):
        return hash(f"{self.title}{self.summary}")

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __ne__(self, other):
        return not self.__eq__(other)


class NewsColorsAndFonts:
    LINE_COLOR = '#1fb6b6'
    GRADIENT_COLOR = '#182419'
    MAIN_COLOR = '#fff'

    FONT_MAIN = 'fonts/Bebas_Neue_Cyrillic.ttf'
