FROM python:3.8.6-alpine as base

ENV PYTHONDONTWRITEBYTECODE 1

COPY app/requirements.txt .
RUN apk add --update --no-cache --virtual .build-deps \
    build-base \
    postgresql-dev \
    python3-dev \
    musl-dev \
    libffi-dev \
    jpeg-dev \
    zlib-dev \
    libpq \
    && \
    pip install --upgrade pip \
    && \
    pip install -r requirements.txt \
    && \
    find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && \
    runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && \
    apk add --virtual .rundeps $runDeps \
    && \
    apk del .build-deps

FROM python:3.8.6-alpine

ARG DEBUG
ARG SECRET_KEY
ARG ALLOWED_HOSTS
ARG ADMIN_EMAIL
ARG ADMIN_NICKNAME
ARG ADMIN_PASSWORD
ARG POSTGRES_DB
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_HOST
ARG POSTGRES_PORT

ENV DEBUG ${DEBUG}
ENV SECRET_KEY ${SECRET_KEY}
ENV ALLOWED_HOSTS ${ALLOWED_HOSTS}
ENV ADMIN_EMAIL ${ADMIN_EMAIL}
ENV ADMIN_NICKNAME ${ADMIN_NICKNAME}
ENV ADMIN_PASSWORD ${ADMIN_PASSWORD}
ENV POSTGRES_DB ${POSTGRES_DB}
ENV POSTGRES_USER ${POSTGRES_USER}
ENV POSTGRES_PASSWORD ${POSTGRES_PASSWORD}
ENV POSTGRES_HOST ${POSTGRES_HOST}
ENV POSTGRES_PORT ${POSTGRES_PORT}

RUN apk add --update --no-cache libpq libjpeg-turbo

COPY --from=base /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH "${PYTHONPATH}:/app/"

COPY /app /app/
COPY bin/docker-entrypoint.sh /app/

EXPOSE 8001

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
