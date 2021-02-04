FROM python:3.8.6-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ENV APP_SECRET development-secret-key
ENV APP_ENV development

RUN mkdir /api
WORKDIR /api

RUN pip install --upgrade pip

COPY api/requirements.txt /api/
RUN pip install -r requirements.txt
COPY api/ /api/

EXPOSE 8001
