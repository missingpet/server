FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - && \
    poetry config virtualenvs.create false

COPY app/poetry.lock app/pyproject.toml /app/
RUN poetry install
COPY app/ /app/
