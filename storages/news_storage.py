from typing import Hashable

from storages.base_storage import BaseStorage


class NewsStorage(BaseStorage):
    STORAGE_FILE_NAME = 'news'

    def store_element(self, element: Hashable):
        data = self.get_data()
        if not data:
            data = dict()

        data[element] = element
        self.save_data(data)
