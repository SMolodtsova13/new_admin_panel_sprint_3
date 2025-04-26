import time
import psycopg2
import psycopg2.extras
from config import DB_CONFIG
from state import State

class PostgresExtractor:
    """
    Извлекает фильмы из Postgres, изменённые после заданного timestamp.
    """
    def __init__(self, state: State):
        """Инициализирует подключение к БД."""
        self.state = state
        while True:
            try:
                self.conn = psycopg2.connect(**DB_CONFIG)
                break
            except psycopg2.OperationalError as e:
                print(f'Не удалось подключиться к PostgreSQL: {e}')
                time.sleep(5)

    def extract_movies(self, updated_since: str):
        """
        Возвращает список dict фильмов с полем 'modified' после updated_since.
        """
        with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute('''
                WITH updated_filmworks AS (
                    SELECT fw.id
                    FROM content.film_work fw
                    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                    WHERE fw.modified > %s
                       OR gfw.created > %s
                       OR pfw.created > %s
                    GROUP BY fw.id
                )
                SELECT fw.id,
                       fw.modified,
                       fw.rating AS imdb_rating,
                       fw.title,
                       fw.description,
                       ARRAY_AGG(DISTINCT g.name) AS genres,
                       ARRAY_AGG(DISTINCT p.id || ':' || p.full_name || ':' || pfw.role) AS persons
                FROM content.film_work fw
                LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                LEFT JOIN content.genre g ON g.id = gfw.genre_id
                LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                LEFT JOIN content.person p ON p.id = pfw.person_id
                WHERE fw.id IN (SELECT id FROM updated_filmworks)
                GROUP BY fw.id
            ''', (updated_since, updated_since, updated_since))

            rows = cur.fetchall()
            result = []

            for row in rows:
                persons = [p.split(':') for p in row['persons'] if p]
                fw = {
                    'id': row['id'],
                    'modified': row['modified'],
                    'imdb_rating': row['imdb_rating'],
                    'title': ('' if row['title'] == 'N/A' else row['title']),
                    'description': ('' if row['description'] == 'N/A' else row['description']),
                    'genres': row['genres'] or [],
                    'actors': [],
                    'writers': [],
                    'directors': [],
                    'actors_names': [],
                    'writers_names': [],
                    'directors_names': [],
                }
                for pid, name, role in persons:
                    person = {'id': pid, 'name': name}
                    fw[role + 's'].append(person)
                    fw[role + 's_names'].append(name)

                result.append(fw)
            return result
