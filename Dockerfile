FROM python:3.8.6-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ENV DJANGO_ENV development

WORKDIR /app

RUN pip install --upgrade pip

COPY app/requirements.txt /app/
RUN pip install -r requirements.txt
COPY app/ /app/

EXPOSE 8000

CMD ["sh", "web.sh"]
