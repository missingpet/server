FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY app/poetry.lock app/pyproject.toml /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install
COPY app/ /app/
