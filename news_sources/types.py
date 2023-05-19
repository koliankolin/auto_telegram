from enum import Enum
from dataclasses import dataclass


@dataclass
class News:
    title: str
    summary: str
    img_url: str


@dataclass
class NYTimesNews(News):
    pass


class NewsColorsAndFonts(Enum):
    LINE_COLOR = '#1fb6b6'
    MAIN_COLOR = '#fff'
    GRADIENT_COLOR = '#182419'

    FONT_LINE = 'fonts/Bebas_Neue_Cyrillic.ttf'
    FONT_MAIN = 'fonts/Bebas_Neue_Cyrillic.ttf'

    INFO = 'ФУТБОЛ: НОВОСТИ И ОБЗОРЫ'
