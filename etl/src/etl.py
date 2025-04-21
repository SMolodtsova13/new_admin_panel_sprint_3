import logging
import time
import os
import sys
import django
from contextlib import closing

from elasticsearch import Elasticsearch
import psycopg2

from extractor import PostgresExtractor
from loader import ElasticsearchLoader
from state import State
from storage import JsonFileStorage
from utils import backoff, prepare_filmworks, load_full_filmworks  
# Настройка Django
sys.path.append('/opt/app/simple_project/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.example.settings')
django.setup()

from django.conf import settings

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


@backoff()
def run_etl():
    # Конфигурация подключения к PostgreSQL
    dsn = {
        "dbname": settings.DATABASES['default']['NAME'],
        "user": settings.DATABASES['default']['USER'],
        "password": settings.DATABASES['default']['PASSWORD'],
        "host": settings.DATABASES['default']['HOST'],
        "port": settings.DATABASES['default']['PORT'],
        "options": settings.DATABASES['default']['OPTIONS']['options'],
    }

    # Инициализация хранилища состояния
    storage = JsonFileStorage(settings.STATE_FILE_PATH)
    state = State(storage)

    with closing(psycopg2.connect(**dsn)) as pg_conn, Elasticsearch(settings.ES_HOST) as es:
        extractor = PostgresExtractor(pg_conn, state)
        loader = ElasticsearchLoader(es, 'movies')

        while True:
            try:
                filmwork_ids = extractor.extract()
                if filmwork_ids:
                    logger.info(f"Extracted {len(filmwork_ids)} filmwork IDs.")

                    # Загрузка полных объектов Filmwork
                    records = load_full_filmworks(pg_conn, filmwork_ids)

                    if not records:
                        logger.warning("No filmwork records loaded. Skipping.")
                        continue

                    documents = prepare_filmworks(records)
                    loader.bulk_upload(documents)

                    logger.info("Uploaded to Elasticsearch.")

                    # Обновление состояния по максимальной дате изменения
                    last_modified = max(fw.modified for fw in records)
                    state.set_state("last_modified", last_modified.isoformat())
                else:
                    logger.info("No new data.")
            except Exception as e:
                logger.exception(f"ETL error: {e}")

            time.sleep(settings.POLL_INTERVAL)


if __name__ == '__main__':
    try:
        logger.info("Starting ETL process...")
        run_etl()
    except KeyboardInterrupt:
        logger.info("ETL process interrupted.")
# # etl.py

# import logging
# import time
# import os
# import sys
# import django
# from contextlib import closing

# from elasticsearch import Elasticsearch
# import psycopg2

# from extractor import PostgresExtractor
# from loader import ElasticsearchLoader
# from state import State
# from storage import JsonFileStorage
# from utils import backoff, prepare_filmworks

# sys.path.append('/opt/app/simple_project/app')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.example.settings')
# django.setup()

# from django.conf import settings

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
# )
# logger = logging.getLogger(__name__)

# # QUERY = """
# # SELECT fw.id, fw.title, fw.description, fw.rating AS imdb_rating, fw.modified
# # FROM content.film_work fw
# # WHERE fw.modified > %s
# # ORDER BY fw.modified;
# # """



# @backoff()
# def run_etl():
#     dsn = {
#         "dbname": settings.DATABASES['default']['NAME'],
#         "user": settings.DATABASES['default']['USER'],
#         "password": settings.DATABASES['default']['PASSWORD'],
#         "host": settings.DATABASES['default']['HOST'],
#         "port": settings.DATABASES['default']['PORT'],
#         "options": settings.DATABASES['default']['OPTIONS']['options'],
#     }

#     storage = JsonFileStorage(settings.STATE_FILE_PATH)
#     state = State(storage)
#     # last_modified = state.get_state("last_modified")

#     with closing(psycopg2.connect(**dsn)) as pg_conn, Elasticsearch(settings.ES_HOST) as es:
#         # extractor = PostgresExtractor(dsn, QUERY)
#         extractor = PostgresExtractor(pg_conn, state)
#         loader = ElasticsearchLoader(es, 'movies')

#         while True:
#             try:
#                 # records = list(extractor.extract(last_modified))
#                 records = extractor.extract()
#                 if records:
#                     logger.info(f"Extracted {len(records)} records.")
#                     documents = prepare_filmworks(records)
#                     loader.bulk_upload(documents)
                    
#                     logger.info("Uploaded to Elasticsearch.")
#                     last_modified = max(record['modified'] for record in records)
#                     state.set_state("last_modified", last_modified.isoformat())
#                 else:
#                     logger.info("No new data.")
#             except Exception as e:
#                 logger.exception(f"ETL error: {e}")

#             time.sleep(settings.POLL_INTERVAL)


# if __name__ == '__main__':
#     try:
#         logger.info("Starting ETL process...")
#         run_etl()
#     except KeyboardInterrupt:
#         logger.info("ETL process interrupted.")


# import logging
# import time
# from contextlib import closing
# import psycopg2
# from elasticsearch import Elasticsearch

# from extractor import PostgresExtractor
# from loader import ElasticsearchLoader
# from models import Filmwork, Person, Genre
# from state import State
# from storage import JsonFileStorage
# from utils import backoff, prepare_filmworks

# import os
# import sys
# import django

# import sys
# import os
# from django.conf import settings

# sys.path.append('/opt/app/simple_project/app')

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.example.settings')
# django.setup()

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
# )
# logger = logging.getLogger(__name__)

# @backoff()
# def run_etl():
#     dsn = {
#         "dbname": settings.DATABASES['default']['NAME'],
#         "user": settings.DATABASES['default']['USER'],
#         "password": settings.DATABASES['default']['PASSWORD'],
#         "host": settings.DATABASES['default']['HOST'],  # <- это важно
#         "port": settings.DATABASES['default']['PORT'],
#         "options": settings.DATABASES['default']['OPTIONS']['options'],
#         # "options": settings.DATABASES['default']['OPTIONS'],
#     }

#     storage = JsonFileStorage(settings.STATE_FILE_PATH)
#     state = State(storage)

#     with closing(psycopg2.connect(**dsn)) as pg_conn, Elasticsearch(hosts=settings.ES_HOST) as es:
#         extractor = PostgresExtractor(pg_conn, state)
#         loader = ElasticsearchLoader(es, settings.ES_INDEX_SCHEMA_PATH)
#         # loader = ElasticsearchLoader(es, settings.ES_INDEX_NAME)

#         while True:
#             try:
#                 changed_ids = extractor.extract()
#                 if changed_ids:
#                     filmworks = extractor.load_filmworks(changed_ids)
#                     logger.info(f"Loaded {len(filmworks)} filmworks")

#                     documents = prepare_filmworks(filmworks)
#                     loader.bulk_upload(documents)
#                     logger.info("Uploaded to Elasticsearch")

#                     state.set_state("last_modified", extractor.last_modified)

#             except Exception as e:
#                 logger.exception(f"ETL error: {e}")

#             time.sleep(settings.poll_interval)


# if __name__ == '__main__':
#     try:
#         logger.info("Starting ETL process...")
#         run_etl()
#     except KeyboardInterrupt:
#         logger.info("ETL process interrupted.")
