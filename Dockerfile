# pull official base image
FROM python:3.8.0-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN ["/bin/bash", "-c", "apk update"]
RUN ["/bin/bash", "-c", "apk add gcc python3-dev musl-dev zlib-dev jpeg-dev mariadb-connector-c-dev libffi-dev"]

COPY . /usr/src/app/

# install dependencies
RUN ["/bin/bash", "-c", "pip install --upgrade pip"]
RUN ["/bin/bash", "-c", "pip install -r requirements.txt"]
