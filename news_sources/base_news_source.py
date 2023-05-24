import os
from typing import Dict, List, Tuple, Optional
from datetime import date
from abc import ABC, abstractmethod
from pathlib import Path
import textwrap
from copy import deepcopy

from bs4 import BeautifulSoup
import requests
from fake_useragent import FakeUserAgent
from telebot import formatting
from PIL import Image, ImageDraw, ImageFont
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from storages.news_storage import NewsStorage
from news_sources.types import News, NewsColorsAndFonts
from rewriters.chatgpt_rewriter import ChatGPTRewriter


class BaseNewsSource(ABC):
    SOURCE = ''
    HASHTAG = ''

    def __init__(self, url: str):
        self.parsed_source = BeautifulSoup(
            requests.get(
                url=url,
                headers=self._get_headers()
            ).content,
            features='lxml'
        )

    def get_news(self) -> List[News]:
        raw_news = self._get_raw_today_news()
        return self._map_raw_news(raw_news=raw_news)

    def get_one_news(self) -> Optional[News]:
        all_news = self.get_news()
        storage = NewsStorage()

        for one_news in all_news:
            if storage.exists_element(element=one_news) or self._is_duplicated_news(one_news=one_news):
                continue

            storage.store_element(element=one_news)
            return self._rewrite_one_news(one_news=one_news)
        return None

    @staticmethod
    def _rewrite_one_news(one_news: News) -> News:
        copy_one_news = deepcopy(one_news)
        rewriter = ChatGPTRewriter()

        new_title = rewriter.rewrite_title(title=one_news.title)
        new_summary = rewriter.rewrite_summary(summary=one_news.summary)

        copy_one_news.title = new_title
        copy_one_news.summary = new_summary

        return copy_one_news

    def construct_caption(self, news: News) -> str:
        return f"{news.summary}\n\n{self._get_footer()}"

    def _get_footer(self) -> str:
        return f"#{self.HASHTAG} | {formatting.hlink('INTERESTING NEWS', 'https://t.me/+V3JQF4Q23u84MGU0')}"

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        ua = FakeUserAgent()

        return {
            'User-Agent': ua.random
        }

    @abstractmethod
    def _get_raw_today_news(self) -> List[BeautifulSoup]:
        pass

    @abstractmethod
    def _map_raw_news(self, raw_news: List[BeautifulSoup]) -> List[News]:
        pass

    @abstractmethod
    def _get_article_url(self, raw_news: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def _get_article_date(self, raw_news: BeautifulSoup) -> date:
        pass

    def _is_fresh_article(self, raw_news: BeautifulSoup) -> bool:
        today = date.today()
        article_date = self._get_article_date(raw_news=raw_news)

        return today == article_date

    def _get_article_soup(self, raw_news: BeautifulSoup) -> BeautifulSoup:
        article_url = self._get_article_url(raw_news=raw_news)
        return BeautifulSoup(
            requests.get(
                url=article_url,
                headers=self._get_headers(),
            ).content,
            features='lxml'
        )

    @abstractmethod
    def _get_title(self, article_soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def _get_summary(self, article_soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def _get_image_url(self, article_soup: BeautifulSoup) -> str:
        pass

    @staticmethod
    def get_images_folder() -> Path:
        return Path(__file__).parent / f"../visualization/"

    @classmethod
    def create_mem_from_photo(
            cls,
            news: News,
            gradient: float = 4.,
            initial_opacity: float = 1.,
            file_name: str = 'out.png'
    ) -> Path:

        image_bytes = requests.get(news.img_url, stream=True).raw

        img = Image.open(image_bytes)
        input_im = img.convert("RGBA")

        if input_im.mode != 'RGBA':
            input_im = input_im.convert('RGBA')
        width, height = input_im.size

        # create gradient
        alpha_gradient = Image.new('L', (1, height), color=0xFF)
        for x, x1 in zip(range(height)[::-1], range(height)):
            a = int((initial_opacity * 255.) * (1. - gradient * float(x) / height))
            if a > 0:
                alpha_gradient.putpixel((0, x1), a)
            else:
                alpha_gradient.putpixel((0, x1), 0)
        alpha = alpha_gradient.resize(input_im.size)

        black_im = Image.new('RGBA', (width, height), color=NewsColorsAndFonts.GRADIENT_COLOR)  # i.e. black
        black_im.putalpha(alpha)

        # make composite with original image
        output_im = Image.alpha_composite(input_im, black_im)

        font_size = 0.075 if width < height else 0.055
        fnt_path = str(cls.get_images_folder() / NewsColorsAndFonts.FONT_MAIN)

        title_font = ImageFont.truetype(fnt_path, int(img.size[0] * (font_size - 0.01)))
        fnt_mir = ImageFont.truetype(fnt_path, int(img.size[0] * (font_size - 0.02)))
        info_font = ImageFont.truetype(fnt_path, int(img.size[0] * (font_size - 0.035)))

        total_text_height, wrapped_text, padding = cls._wrap_text_and_get_total_height(
            image=img,
            text=news.title,
            title_font=title_font,
            source_font=info_font
        )

        new_image_height = int(img.size[1] + total_text_height)
        overlay = Image.new('RGBA', (img.size[0], new_image_height), NewsColorsAndFonts.GRADIENT_COLOR)
        overlay.paste(output_im, (0, 0))

        img = overlay
        d = ImageDraw.Draw(img)

        width_source = d.textlength(cls.SOURCE, font=fnt_mir)
        height_source = fnt_mir.getbbox(cls.SOURCE)[-1] + padding
        txt_height = new_image_height - total_text_height - height_source
        d.text(((img.size[0] - width_source) / 2, txt_height), cls.SOURCE, font=fnt_mir,
               fill=NewsColorsAndFonts.LINE_COLOR)

        current_h = new_image_height - total_text_height

        for line in wrapped_text:
            w = d.textlength(line, font=title_font)
            h = title_font.getbbox(line)[-1]
            d.text(((img.size[0] - w) / 2, current_h), line, font=title_font,
                   fill=NewsColorsAndFonts.MAIN_COLOR)
            current_h += h + padding

        top = (15, txt_height * 1.03)
        x = (width // 2) - width_source
        left = (x, txt_height * 1.03)

        x1 = x + width_source * 2
        top1 = (x1, txt_height * 1.03)
        left1 = (width - 15, txt_height * 1.03)

        top2 = (15, img.size[1] - 10)
        left2 = (width - 15, new_image_height - 10)

        d.line([top, left], fill=NewsColorsAndFonts.LINE_COLOR, width=3)
        d.line([top1, left1], fill=NewsColorsAndFonts.LINE_COLOR, width=3)
        d.line([top2, left2], fill=NewsColorsAndFonts.LINE_COLOR, width=3)

        path_out = cls.get_images_folder() / file_name
        img.save(path_out.absolute(), 'PNG')

        return path_out.absolute()

    @classmethod
    def _wrap_text_and_get_total_height(
            cls,
            image: Image,
            text: str,
            title_font: ImageFont.FreeTypeFont,
            source_font: ImageFont.FreeTypeFont
    ) -> Tuple[int, List[str], int]:
        avg_symbol_length = title_font.getlength(text) // len(text)
        width_line = image.size[0] * 0.9
        wrap_width = width_line // avg_symbol_length
        padding = image.size[1] * 0.01

        wrapped_text = textwrap.wrap(text, width=wrap_width)

        total_height = 0
        for line in wrapped_text:
            h = title_font.getbbox(line)[-1]
            total_height += h + padding

        info_height = source_font.getbbox(cls.SOURCE)[-1]
        total_height += info_height

        return total_height, wrapped_text, padding

    @staticmethod
    def _is_duplicated_news(one_news: News) -> bool:
        storage = NewsStorage()
        data_from_storage = storage.get_data()
        if not data_from_storage:
            return False

        news_from_storage = list(data_from_storage.keys())
        corpus = [
            f"{one_news.title} {one_news.summary}"
            for one_news in news_from_storage[-35:]
        ]
        corpus.append(f"{one_news.title} {one_news.summary}")

        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
        cosine_sim_values = cosine_similarity(tfidf_matrix, tfidf_matrix)[-1][:-1]

        threshold = float(os.environ.get("DEDUPLICATION_THRESHOLD") or 0.3)
        return any([cosine_sim_value for cosine_sim_value in cosine_sim_values if cosine_sim_value > threshold])
