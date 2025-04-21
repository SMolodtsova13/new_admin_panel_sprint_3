import psycopg2
from typing import List
from models import Filmwork, Genre, Person

import functools
import time
import logging


def backoff(start_sleep_time=1, factor=2, border_sleep_time=60):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = start_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.warning(f"Error: {e}, retrying in {delay} seconds")
                    time.sleep(delay)
                    delay = min(delay * factor, border_sleep_time)
        return wrapper
    return decorator

def get_modified_filmwork_ids(conn, last_modified: str) -> List[str]:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT DISTINCT fw.id
            FROM content.film_work fw
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
            WHERE fw.modified > %s;
        """, (last_modified,))
        return [row[0] for row in cur.fetchall()]

#         cur.execute("""
#             SELECT DISTINCT fw.id
#             FROM content.film_work fw
#             WHERE fw.modified > %s;
#         """,

def load_full_filmworks(conn, ids: List[str]) -> List[Filmwork]:
    if not ids:
        return []

    with conn.cursor() as cur:
        query = """
            SELECT fw.id, fw.title, fw.description, fw.rating, fw.modified,
                   g.id AS genre_id, g.name AS genre_name,
                   p.id AS person_id, p.full_name, pfw.role
            FROM content.film_work fw
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
            LEFT JOIN content.genre g ON g.id = gfw.genre_id
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.person p ON p.id = pfw.person_id
            WHERE fw.id = ANY(%s);
        """
        cur.execute(query, (ids,))
        rows = cur.fetchall()

    filmworks = {}
    for row in rows:
        fw_id = row[0]
        if fw_id not in filmworks:
            filmworks[fw_id] = Filmwork(
                id=row[0], title=row[1], description=row[2],
                imdb_rating=row[3], modified=row[4]
            )
        fw = filmworks[fw_id]

        if row[5] and row[6]:
            genre = Genre(id=row[5], name=row[6])
            if genre not in fw.genre:
                fw.genre.append(genre)

        if row[7] and row[8] and row[9]:
            person = Person(id=row[7], name=row[8])
            role = row[9]
            if person not in getattr(fw, role + 's'):
                getattr(fw, role + 's').append(person)

    return list(filmworks.values())

def prepare_filmworks(filmworks: List[Filmwork]) -> List[dict]:
    return [
        {
            "id": fw.id,
            "title": fw.title,
            "description": fw.description,
            "imdb_rating": fw.imdb_rating,
            "genre": [g.name for g in fw.genre],
            "genre_ids": [g.id for g in fw.genre],
            "actors": [p.name for p in fw.actors],
            "actors_ids": [p.id for p in fw.actors],
            "writers": [p.name for p in fw.writers],
            "writers_ids": [p.id for p in fw.writers],
            "directors": [p.name for p in fw.directors],
            "directors_ids": [p.id for p in fw.directors],
        } for fw in filmworks
    ]
