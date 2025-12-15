FROM python:3.12
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt && apt-get update -q
RUN apt-get install -y wget libpq-dev gcc

RUN rm -rf /etc/localtime
RUN ln -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime
RUN echo "Europe/Moscow" > /etc/timezone

RUN mkdir -p /app/logs

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

ARG WORKERS

CMD fastapi run --workers $WORKERS main.py
