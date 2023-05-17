from typing import List, Any

from bs4 import BeautifulSoup

from news_sources.base_news_source import BaseNewsSource
from news_sources.types import NYTimesNews


class NYTimesNewsSource(BaseNewsSource):
    SOURCE_MAIN_URL = 'https://www.nytimes.com/'
    SOURCE = 'New York Time'

    def __init__(self):
        super().__init__(url='https://www.nytimes.com/section/world')

    def _get_raw_today_news(self) -> List[Any]:
        return self.parsed_source.find_all(name='div', attrs={'class': 'css-1cp3ece'})

    def _map_raw_news(self, raw_news: List[Any]) -> List[NYTimesNews]:
        result = []
        for raw_one_news in raw_news:
            article_soup = self._get_article_soup(raw_news=raw_one_news)
            try:
                result.append(
                    NYTimesNews(
                        title=self._get_title(article_soup),
                        summary=self._get_summary(article_soup),
                        img_url=self._get_image_url(article_soup)
                    )
                )
            except Exception:
                pass

        return result

    def _get_article_url(self, raw_news: BeautifulSoup) -> str:
        url_end = raw_news.find(name='a').attrs['href']
        return f"{self.SOURCE_MAIN_URL}{url_end}"

    def _get_title(self, article_soup: BeautifulSoup) -> str:
        return article_soup.find(name='h1').text

    def _get_summary(self, article_soup: BeautifulSoup) -> str:
        return article_soup.find(name='p', attrs={'id': 'article-summary'}).text

    def _get_image_url(self, article_soup: BeautifulSoup) -> str:
        return article_soup.find(name='img').attrs['srcset'].split(',')[-1].split('?')[0]
