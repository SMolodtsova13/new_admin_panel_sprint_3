import logging
import time

from config import ES_HOST, ES_INDEX, ES_INDEX_BODY, STATE_FILE_PATH
from elasticsearch import Elasticsearch
from extractor import PostgresExtractor
from loader import ESLoader
from models import FilmWork
from state import State
from storage import JsonFileStorage
from utils import chunked

RETRY_DELAY = 5  # задержка между циклами
BATCH_SIZE = 100  # размер пакета для bulk

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main():
    """
    Запуск ETL: считывает обновления из PostgreSQL и загружает в Elasticsearch.
    1. Читает последний timestamp из состояния.
    2. Проверяет и создаёт индекс, если нужно.
    3. В цикле: извлекает, преобразует, бандлит и обновляет состояние.
    """
    logging.info('ETL-сервис запущен')
    # Инициализация состояния и экстрактора
    storage = JsonFileStorage(STATE_FILE_PATH)
    state = State(storage)
    extractor = PostgresExtractor(state)

    # Создаём клиент Elasticsearch и автоматически создаём индекс, если его нет
    es = Elasticsearch(ES_HOST)
    if not es.indices.exists(index=ES_INDEX):
        es.indices.create(index=ES_INDEX, body=ES_INDEX_BODY)
        logging.info(f'Создан новый индекс: {ES_INDEX}')
    else:
        logging.info(f'Индекс уже существует: {ES_INDEX}')

    # инициализируем загрузчик (он берёт ES_HOST и ES_INDEX из config)
    loader = ESLoader()

    while True:
        last_modified = state.get('modified') or '1900-01-01'

        # Получаем список dict с ключом 'modified'
        raw_data = extractor.extract_movies(last_modified)

        logging.info(f'Выгружено записей из БД: {len(raw_data)}')

        if not raw_data:
            logging.info('Новых данных нет. Ожидание следующей попытки...')
            time.sleep(RETRY_DELAY)
            continue

        # Вычисляем новую точку останова
        latest = max(
            (
                row.get('modified') for row in raw_data if row.get('modified')
            ), default=None
        )

        # Создаём объекты FilmWork без поля modified
        filmworks = [
            FilmWork(**{k: v for k, v in row.items() if k != 'modified'})
            for row in raw_data
        ]

        # Загрузка в ES
        for batch in chunked(filmworks, BATCH_SIZE):
            loader.load(batch)
            logging.info(f'Загружено в Elasticsearch: {len(batch)} записей')

        if latest is not None:
            state.set('modified', latest.isoformat())
            logging.info(
                f'Обновлено состояние: modified = {latest.isoformat()}'
            )

        time.sleep(RETRY_DELAY)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.exception(f'Ошибка в ETL процессе: {e}')
        time.sleep(RETRY_DELAY)
