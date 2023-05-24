from abc import ABC, abstractmethod
from typing import Hashable, Optional, Dict
from pathlib import Path
import pickle


class BaseStorage(ABC):
    STORAGE_FILE_NAME = ''

    @staticmethod
    def _get_storages_folder() -> Path:
        return Path(__file__).parent / "../data"

    def _create_storages_folder(self):
        self._get_storages_folder().mkdir(parents=True, exist_ok=True)

    def _get_storage_file_name(self) -> Path:
        return self._get_storages_folder() / self.STORAGE_FILE_NAME

    @abstractmethod
    def store_element(self, element: Hashable):
        pass

    def exists_element(self, element: Hashable) -> bool:
        data = self.get_data()
        return element in data if data else False

    def save_data(self, data: Dict):
        if not self._get_storages_folder().exists():
            self._create_storages_folder()
        with open(self._get_storage_file_name(), 'wb') as f:
            pickle.dump(data, f)

    def get_data(self) -> Optional[Dict]:
        if self._get_storage_file_name().exists():
            with open(self._get_storage_file_name(), 'rb') as f:
                return pickle.load(f)
        return None
