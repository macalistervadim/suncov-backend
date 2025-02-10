FROM python:3.13-slim as builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN pip install poetry
RUN poetry --version

FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY . /app/

ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["gunicorn", "src.config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
