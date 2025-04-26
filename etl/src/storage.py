import json
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


class JsonFileStorage:
    """Класс для хранения состояния в JSON-файле."""
    def __init__(self, file_path: str):
        if os.path.isdir(file_path):
            raise RuntimeError(
                f'ОШИБКА: путь "{file_path}" — директория, а ожидался файл. '
                'Проверь настройки volumes и переменную STATE_FILE_PATH.'
            )
        self.file_path = file_path

        # Если файла нет — создаём пустой файл
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            logger.info(f'Создан новый файл состояния: {self.file_path}')

        self.data = self._load()

    def _load(self) -> dict:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logger.warning(f'Проблема с {self.file_path}. '
                           'Используется пустое состояние.')
            return {}

    def save(self, data: dict):
        """Сохраняет состояние в JSON-файл."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def get_state(self) -> dict:
        return self.data

    def set_state(self, key: str, value: Any):
        self.data[key] = value
        self.save(self.data)
