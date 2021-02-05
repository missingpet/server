FROM python:3.8.6-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /api

RUN pip install --upgrade pip

COPY api/requirements.txt /api/
RUN pip install -r requirements.txt
COPY api/ /api/

RUN if [ "${APP_ENV}" = "production" ]; then \
        apt-get update \
        && \
        apt-get add libpq libssl gcc \
        && \
        pip install psycopg2==2.8.6 ; \
        fi

EXPOSE 8001