# Заключительное задание первого модуля

Ваша задача в этом уроке — загрузить данные в Elasticsearch из PostgreSQL. Подробности задания в папке `etl`.

project_root/
├── .env
├── docker-compose.yml
├── database_dump.sql
├── etl/
│   ├── Dockerfile
│   ├── state.json
│   └── src/
│       ├── __init__.py
│       ├── config.py
│       ├── etl.py
│       ├── extractor.py
│       ├── loader.py
│       ├── models.py
│       ├── state.py
│       ├── storage.py
│       └── utils.py
├── simple_project/
│   ├── app/
│   │   ├── Dockerfile
│   │   └── ... (Django project files)
│   └── nginx/
│       ├── nginx.conf
│       └── conf.d/
│           └── site.conf
└── nginx/
    ├── nginx.conf
    └── conf.d/
        └── site.conf
