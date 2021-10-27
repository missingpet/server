FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get -y install libpq-dev gcc

WORKDIR /app

RUN pip install poetry

COPY ./poetry.lock ./pyproject.toml ./
RUN poetry config virtualenvs.create false && \
    poetry install
COPY . .

RUN chmod a+x ./docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]

CMD ["gunicorn", "conf.wsgi"]