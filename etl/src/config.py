# import os

# DB_DSL = {
#     'dbname': os.getenv('POSTGRES_DB', 'theatre'),
#     'user': os.getenv('POSTGRES_USER', 'postgres'),
#     'password': os.getenv('POSTGRES_PASSWORD', 'secret'),
#     'host': os.getenv('SQL_HOST', 'localhost'),
#     'port': int(os.getenv('SQL_PORT', 5432)),
#     'options': os.getenv('SQL_OPTIONS', '-c search_path=content')
# }


# @backoff()
# def run_etl():
#     dsn = {
#         "dbname": settings.DATABASES['default']['NAME'],
#         "user": settings.DATABASES['default']['USER'],
#         "password": settings.DATABASES['default']['PASSWORD'],
#         "host": settings.DATABASES['default']['HOST'],
#         "port": settings.DATABASES['default']['PORT'],
#         # "options": settings.DATABASES['default']['OPTIONS'],
#         "options": settings.DATABASES['default']['OPTIONS'] if settings.DATABASES['default']['OPTIONS'] else '',

#         # "options": settings.DATABASES['default']['OPTIONS'].split('=')[1] if settings.DATABASES['default']['OPTIONS'] else '',
#     }


# ES_HOST = os.getenv('ES_HOST', 'http://elasticsearch:9200')
# STATE_FILE_PATH = os.getenv('STATE_FILE_PATH', 'state.json')
