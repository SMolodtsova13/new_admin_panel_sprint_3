import logging
import time

import psycopg2
import psycopg2.extras

from config import DB_CONFIG
from state import State

logger = logging.getLogger(__name__)


class PostgresExtractor:
    """
    Извлекает фильмы из Postgres, изменённые после заданного timestamp.
    Поддерживает поэтапную выгрузку данных.
    """
    def __init__(
            self,
            state: State,
            max_retries: int = 5,
            retry_delay: int = 5
    ):
        """
        Инициализирует подключение к БД с ограниченным числом попыток.
        Args:
            state (State): менеджер состояния для чтения чекпоинта.
            max_retries (int): максимум попыток подключения.
            retry_delay (int): задержка между попытками (в секундах).
        """
        self.state = state
        attempts = 0
        while attempts < max_retries:
            try:
                self.conn = psycopg2.connect(**DB_CONFIG)
                return
            except psycopg2.OperationalError as e:
                logger.error(
                    f'Не удалось подключиться к БД (попытка {attempts+1}): {e}'
                )
                attempts += 1
                time.sleep(retry_delay)
        raise ConnectionError(
            f'Не удалось подключиться к БД после {max_retries} попыток'
        )

    def extract_movies(self, updated_since: str):
        """
        Возвращает список dict фильмов с полем 'modified' после updated_since.
        Использует fetchmany для батчевой выгрузки.
        Args:
            updated_since (str): ISO timestamp для фильтрации.
        Returns:
            List[dict]: список фильмов с вложенным полем 'modified'.
        """
        result = []
        with self.conn.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cur:
            cur.execute('''
                WITH updated_filmworks AS (
                        SELECT fw.id,
                            GREATEST(
                                MAX(fw.modified),
                                MAX(gfw.created),
                                MAX(pfw.created)
                            ) AS max_modified
                    FROM content.film_work fw
                    LEFT JOIN content.genre_film_work gfw ON
                        gfw.film_work_id = fw.id
                    LEFT JOIN content.person_film_work pfw ON
                        pfw.film_work_id = fw.id
                    GROUP BY fw.id
                    HAVING GREATEST(
                        MAX(fw.modified),
                        MAX(gfw.created),
                        MAX(pfw.created)
                    ) > %s
                )
                SELECT fw.id,
                       ufw.max_modified AS modified,
                       fw.rating AS imdb_rating,
                       fw.title,
                       fw.description,
                       ARRAY_AGG(DISTINCT g.name) AS genres,
                       ARRAY_AGG(
                        DISTINCT p.id || ':' || p.full_name || ':' || pfw.role
                        ) AS persons
                FROM content.film_work fw
                JOIN updated_filmworks ufw ON ufw.id = fw.id
                LEFT JOIN content.genre_film_work gfw ON
                        gfw.film_work_id = fw.id
                LEFT JOIN content.genre g ON
                        g.id = gfw.genre_id
                LEFT JOIN content.person_film_work pfw ON
                        pfw.film_work_id = fw.id
                LEFT JOIN content.person p ON p.id = pfw.person_id
                GROUP BY fw.id, ufw.max_modified, fw.rating, fw.title, fw.description
            ''', (updated_since,))

            fetch_size = 100
            rows = cur.fetchmany(fetch_size)
            while rows:
                for row in rows:
                    persons = [p.split(':') for p in row['persons'] if p]
                    fw = {
                        'id': row['id'],
                        'modified': row['modified'],
                        'imdb_rating': row['imdb_rating'],
                        'title': '' if row['title'] == 'N/A' else row['title'],
                        'description': '' if row['description'] == 'N/A' else row['description'],
                        'genres': row['genres'] or [],
                        'actors': [],
                        'writers': [],
                        'directors': [],
                        'actors_names': [],
                        'writers_names': [],
                        'directors_names': [],
                    }
                    for pid, name, role in persons:
                        fw[f"{role}s"].append({'id': pid, 'name': name})
                        fw[f"{role}s_names"].append(name)
                    result.append(fw)
                rows = cur.fetchmany(fetch_size)
        return result
