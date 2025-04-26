import time
from elasticsearch import Elasticsearch
from config import STATE_FILE_PATH, ES_HOST, ES_INDEX, ES_INDEX_BODY
from extractor import PostgresExtractor
from loader import ESLoader
from storage import JsonFileStorage
from state import State
from models import FilmWork
from utils import chunked

RETRY_DELAY = 5  # задержка между циклами
BATCH_SIZE = 100  # размер пакета для bulk


def main():
    """
    Запуск ETL: считывает обновления из PostgreSQL и загружает в Elasticsearch.
    1. Читает последний timestamp из состояния.
    2. Проверяет и создаёт индекс, если нужно.
    3. В цикле: извлекает, преобразует, бандлит и обновляет состояние.
    """
    # --- инициализация состояния и экстрактора
    storage = JsonFileStorage(STATE_FILE_PATH)
    state = State(storage)
    extractor = PostgresExtractor(state)

    # --- создаём клиент Elasticsearch и автоматически создаём индекс, если его нет
    es = Elasticsearch(ES_HOST)
    if not es.indices.exists(index=ES_INDEX):
        es.indices.create(index=ES_INDEX, body=ES_INDEX_BODY)

    # --- инициализируем загрузчик (он берёт ES_HOST и ES_INDEX из config)
    loader = ESLoader()

    while True:
        last_modified = state.get('modified') or '1900-01-01'

        # получаем список dict с ключом 'modified'
        raw_data = extractor.extract_movies(last_modified)

        # вычисляем новую точку останова
        latest = max((row['modified'] for row in raw_data), default=None)

        # создаём объекты FilmWork без поля modified
        filmworks = [
            FilmWork(**{k: v for k, v in row.items() if k != 'modified'})
            for row in raw_data
        ]

        # загрузка в ES
        for batch in chunked(filmworks, BATCH_SIZE):
            loader.load(batch)

        # обновляем состояние, если были фильмы
        if latest is not None:
            state.set('modified', latest.isoformat())

        time.sleep(RETRY_DELAY)


if __name__ == '__main__':
    main()
