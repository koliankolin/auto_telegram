from news_sources.nytimes_news_source.base_nytimes_news_source import BaseNYTimesNewsSource


class WorldNYTimesNewsSource(BaseNYTimesNewsSource):
    HASHTAG = 'WORLD'

    def __init__(self):
        super().__init__(url='https://www.nytimes.com/section/world')
