FROM python:3.13.1-slim

WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  POETRY_VERSION=2.0.0 \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN apt-get update && apt-get install -y \
    libpq-dev gcc --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock /app/
RUN pip install "poetry==$POETRY_VERSION" && poetry config virtualenvs.create false && poetry install --no-dev

COPY web /app/

RUN chmod +x /app/entrypoint.py

EXPOSE 8000

ENTRYPOINT ["./entrypoint.py"]