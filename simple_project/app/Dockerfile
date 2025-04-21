FROM python:3.10-slim

WORKDIR /opt/app

# Системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpcre3-dev \
    libssl-dev \
    zlib1g-dev \
    libxml2-dev \
    libsqlite3-dev \
    libpq-dev \
    libcurl4-openssl-dev \
    uuid-dev \
    pkg-config \
    mailcap \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES=1
ENV UWSGI_THREADS=16
ENV UWSGI_HARAKIRI=240
ENV DJANGO_SETTINGS_MODULE=example.settings

COPY requirements.txt /opt/app/
RUN pip install uwsgi==2.0.20 \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY run_uwsgi.sh /opt/app/run_uwsgi.sh
RUN chmod +x /opt/app/run_uwsgi.sh
COPY uwsgi/uwsgi.ini /opt/app/uwsgi.ini

RUN mkdir -p /var/www/static/ \
    && mkdir -p /var/www/media/ \
    && mkdir -p /opt/app/static/ \
    && mkdir -p /opt/app/media/

COPY . /opt/app

RUN apt-get update && apt-get install -y netcat-traditional

RUN chown -R www-data:www-data /opt/app /var/www/static /var/www/media

USER www-data

ENTRYPOINT ["bash", "/opt/app/run_uwsgi.sh"]

CMD ["theatre-db", "5432"]
