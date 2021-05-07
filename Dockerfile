FROM python:3.8.6-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY app/requirements.txt /app/
RUN pip install -r requirements.txt
COPY app/ /app/
