FROM python:3.11-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория внутри контейнера
WORKDIR /opt/app

# Создаём пустой state.json, чтобы volume мог его заменить файлом, а не папкой
RUN touch state.json

# Копируем requirements.txt и устанавливаем зависимости
COPY etl/requirements.txt /opt/app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY etl /opt/app/

# Установка переменной окружения для Python
ENV PYTHONPATH="/opt/app/src"

# Команда запуска
CMD ["python", "src/etl.py"]
 


# FROM python:3.11-slim

# # Установка зависимостей системы
# RUN apt-get update && apt-get install -y \
#     gcc \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# # COPY wait-for-it.sh /wait-for-it.sh
# # RUN chmod +x /wait-for-it.sh

# # Рабочая директория внутри контейнера
# WORKDIR /opt/app

# # Копируем requirements.txt из Django-проекта
# COPY etl/requirements.txt /opt/app/
# RUN pip install --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt

# # Копируем весь код ETL и Django в контейнер
# COPY . /opt/app/
# # COPY simple_project /opt/app/simple_project
# # COPY ../simple_project /opt/app/simple_project

# # Установка переменной окружения для Python
# ENV PYTHONPATH="/opt/app:/opt/app/simple_project"

# CMD ["python", "src/etl.py"]


