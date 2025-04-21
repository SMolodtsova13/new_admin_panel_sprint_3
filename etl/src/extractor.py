# import psycopg2
# from psycopg2.extras import RealDictCursor
# from typing import Generator, Any


# class PostgresExtractor:
#     def __init__(self, dsl: dict, query: str):
#         self.dsl = dsl
#         self.query = query

#     def extract(self, last_modified: str = None) -> Generator[dict, Any, None]:
#         dsl = self.dsl.copy()
#         with psycopg2.connect(**dsl, cursor_factory=RealDictCursor) as conn:
#             with conn.cursor() as cur:
#                 cur.execute(self.query, (last_modified,) if last_modified else ())
#                 while rows := cur.fetchmany(100):
#                     for row in rows:
#                         yield dict(row)

# extractor.py
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Generator, Any
from models import Filmwork
from utils import get_modified_filmwork_ids, load_full_filmworks
from state import State


# class PostgresExtractor:
#     def __init__(self, dsl: dict, query: str):
#         self.dsl = dsl
#         self.query = query

#     def extract(self, last_modified: str = None) -> Generator[dict, Any, None]:
#         with psycopg2.connect(**self.dsl, cursor_factory=RealDictCursor) as conn:
#             with conn.cursor() as cur:
#                 cur.execute(self.query, (last_modified,) if last_modified else ('1970-01-01',))
#                 while rows := cur.fetchmany(100):
#                     for row in rows:
#                         yield dict(row)

class PostgresExtractor:
    def __init__(self, conn, state: State):
        self.conn = conn
        self.state = state
        self.last_modified = state.get_state("last_modified") or "2000-01-01"

    def extract(self) -> List[str]:
        return get_modified_filmwork_ids(self.conn, self.last_modified)
        

    def load_filmworks(self, ids: List[str]) -> List[Filmwork]:
        return load_full_filmworks(self.conn, ids)
