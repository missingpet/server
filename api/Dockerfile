FROM python:3.8.6-alpine

LABEL maintainer="MissingPet"
LABEL version="1.0"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ARG APP_HOSTS
ARG APP_SECRET

ENV APP_ENV production
ENV APP_HOSTS ${APP_HOSTS}
ENV APP_SECRET ${APP_SECRET}

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR ${API_PATH}

ENV SSL_PATH ${API_PATH}ssl/
ENV CRT_PATH ${SSL_PATH}api.crt
ENV KEY_PATH ${SSL_PATH}api.key

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install - r requirements.txt
COPY . .

EXPOSE 8001

ENTRYPOINT ["sh", "docker-entrypoint.sh"]