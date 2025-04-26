from typing import Any

from storage import JsonFileStorage


class State:
    """Читает и сохраняет в JSON-файл."""
    def __init__(self, storage: JsonFileStorage):
        self.storage = storage

    def get(self, key: str) -> Any:
        return self.storage.get_state().get(key)

    def set(self, key: str, value: Any):
        self.storage.set_state(key, value)
