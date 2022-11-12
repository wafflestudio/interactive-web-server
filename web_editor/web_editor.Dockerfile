# pull official base image
FROM python:3.8
# python:3.8.0-alpine

# set work directory
#WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST "redis"

#RUN apt-get update
RUN apt-get install -y bash libjpeg-dev libmariadb3 libmariadb-dev
# graphviz libgraphviz-dev

COPY . /usr/src/app/
# set work directory
WORKDIR /usr/src/app

# install dependencies
#RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -U 'Twisted[tls,http2]'
RUN python3 manage.py makemigrations && python3 manage.py migrate
