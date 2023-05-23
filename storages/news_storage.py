from typing import Hashable

from storages.base_storage import BaseLiveStorage


class NewsStorage(BaseLiveStorage):
    STORAGE_FILE_NAME = 'news'

    def store_element(self, element: Hashable):
        data = self.get_data()
        if not data:
            data = dict()

        data[element] = element
        self.save_data(data)


if __name__ == '__main__':
    from news_sources.types import News

    storage = NewsStorage()
    # storage.store_element(News(
    #     title='title',
    #     summary='summary',
    #     img_url=''
    # ))
    # storage.store_element(News(
    #     title='title1',
    #     summary='summary',
    #     img_url=''
    # ))
    print(storage.get_data())
