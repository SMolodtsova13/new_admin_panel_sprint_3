# import abc
# import json
# import os
# from typing import Any, Dict


# class BaseStorage(abc.ABC):
#     """Абстрактное хранилище состояния."""

#     @abc.abstractmethod
#     def save_state(self, state: Dict[str, Any]) -> None:
#         """Сохранить состояние в хранилище."""

#     @abc.abstractmethod
#     def retrieve_state(self) -> Dict[str, Any]:
#         """Получить состояние из хранилища."""


# class JsonFileStorage(BaseStorage):
#     """Хранилище состояния на базе JSON-файла."""

#     def __init__(self, file_path: str) -> None:
#         self.file_path = file_path

#     def save_state(self, state: Dict[str, Any]) -> None:
#         try:
#             with open(self.file_path, 'w', encoding='utf-8') as file:
#                 json.dump(state, file, ensure_ascii=False, indent=4)
#         except (OSError, IOError) as e:
#             print(f"Ошибка при сохранении состояния: {e}")

#     def retrieve_state(self) -> Dict[str, Any]:
#         if not os.path.exists(self.file_path):
#             return {}
#         try:
#             with open(self.file_path, 'r', encoding='utf-8') as file:
#                 return json.load(file)
#         except (json.JSONDecodeError, OSError, IOError) as e:
#             print(f"Ошибка при загрузке состояния: {e}")
#             return {}


# class State:
#     """Класс для управления состоянием."""

#     def __init__(self, storage: BaseStorage) -> None:
#         self.storage = storage
#         self._state = self.storage.retrieve_state()

#     def set_state(self, key: str, value: Any) -> None:
#         self._state[key] = value
#         self.storage.save_state(self._state)

#     def get_state(self, key: str) -> Any:
#         return self._state.get(key)

from typing import Any
from storage import BaseStorage


class State:
    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage
        self._state = self.storage.retrieve_state()

    def set_state(self, key: str, value: Any) -> None:
        self._state[key] = value
        self.storage.save_state(self._state)

    def get_state(self, key: str) -> Any:
        return self._state.get(key)
