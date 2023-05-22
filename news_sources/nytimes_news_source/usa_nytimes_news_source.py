from news_sources.nytimes_news_source.base_nytimes_news_source import BaseNYTimesNewsSource


class USANYTimesNewsSource(BaseNYTimesNewsSource):
    HASHTAG = 'USA'

    def __init__(self):
        super().__init__(url='https://www.nytimes.com/international/section/us')
