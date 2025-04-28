FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/app

RUN touch state.json

COPY etl/requirements.txt /opt/app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY etl /opt/app/

ENV PYTHONPATH="/opt/app/src"

CMD ["python", "src/etl.py"]
