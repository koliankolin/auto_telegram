from typing import Dict, List
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
import requests
from fake_useragent import FakeUserAgent

from new_sources.types import News


class BaseNewsSource(ABC):
    def __init__(self, url: str):
        self.parsed_source = BeautifulSoup(
            requests.get(
                url=url,
                headers=self._get_headers()
            ).content,
            features="lxml"
        )

    def get_news(self) -> List[News]:
        raw_news = self._get_raw_today_news()
        return self._map_raw_news(raw_news)

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        ua = FakeUserAgent()

        return {
            "User-Agent": ua.random
        }

    @abstractmethod
    def _get_raw_today_news(self) -> List[BeautifulSoup]:
        pass

    @abstractmethod
    def _map_raw_news(self, raw_news: List[BeautifulSoup]) -> List[News]:
        pass