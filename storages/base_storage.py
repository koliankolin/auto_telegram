from abc import ABC, abstractmethod
from typing import Hashable, Optional
from pathlib import Path
import pickle


class BaseLiveStorage(ABC):
    STORAGE_FILE_NAME = ''

    @classmethod
    def _create_live_data_folder(cls):
        cls._get_live_storages_folder().mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _get_live_storages_folder() -> Path:
        return Path(__file__).parent / f"../data/"

    def _get_live_storage_file_name(self) -> Path:
        return self._get_live_storages_folder() / self.STORAGE_FILE_NAME

    @abstractmethod
    def store_element(self, element: Hashable):
        pass

    def exists_element(self, element: Hashable) -> bool:
        data = self.get_data()
        return element in data if data else False

    def save_data(self, data: Hashable):
        if not self._get_live_storages_folder().exists():
            self._create_live_data_folder()
        with open(self._get_live_storage_file_name(), 'wb') as f:
            pickle.dump(data, f)

    def get_data(self) -> Optional[Hashable]:
        if self._get_live_storage_file_name().exists():
            with open(self._get_live_storage_file_name(), 'rb') as f:
                return pickle.load(f)
        return None
