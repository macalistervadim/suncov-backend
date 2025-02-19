# Stage 1: Build (Poetry, зависимости)
FROM python:3.12-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git gettext locales && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-dev

# Stage 2: Production
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gettext locales && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local /usr/local

COPY . /app/

RUN poetry install --no-root --no-dev

ENV PYTHONPATH="/usr/local/lib/python3.12/site-packages"

EXPOSE 8000

CMD ["gunicorn", "src.config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
