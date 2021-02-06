FROM python:3.8.6-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

EXPOSE 8001

ENTRYPOINT ["bash", "bin/docker-entrypoint.sh"]