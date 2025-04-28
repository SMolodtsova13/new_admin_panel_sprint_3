import logging

import backoff
from config import ES_HOST, ES_INDEX
from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import ConnectionError as ESConnError
from elasticsearch.exceptions import TransportError
from models import FilmWork

logger = logging.getLogger(__name__)


class ESLoader:
    """
    Загружает список FilmWork в Elasticsearch через bulk API с retry на сбои.
    """
    def __init__(self):
        self.client = Elasticsearch(ES_HOST)

    @backoff.on_exception(
        backoff.expo,
        (ESConnError, TransportError),
        max_time=60,
        jitter=None
    )
    def load(self, data: list[FilmWork]):
        """
        Индексирует пачку фильмов в указанный индекс.
        При сбое соединения будет пытаться снова по экспоненциальному backoff.
        """
        try:
            actions = [
                {
                    '_index': ES_INDEX,
                    '_id': str(fw.id),
                    '_source': fw.__dict__,
                }
                for fw in data
            ]
            helpers.bulk(self.client, actions)
            logger.info(f'Bulk-загрузка прошла успешно: {len(data)} записей')
        except Exception as e:
            logger.error(f'Ошибка при bulk-загрузке: {e}')
            raise
