from elasticsearch import Elasticsearch, helpers
from config import ES_HOST, ES_INDEX
from models import FilmWork

class ESLoader:
    """
    Загружает список FilmWork в Elasticsearch через bulk API.
    """
    def __init__(self):
        self.client = Elasticsearch(ES_HOST)

    def load(self, data: list[FilmWork]):
        """Индексирует пачку фильмов в указанный индекс."""
        actions = [
            {
                '_index': ES_INDEX,
                '_id': str(fw.id),
                '_source': fw.__dict__,
            }
            for fw in data
        ]
        helpers.bulk(self.client, actions)
