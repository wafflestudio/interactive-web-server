# pull official base image
FROM python:3
# python:3.8.0-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update 
RUN apt-get install -y bash gcc python3-dev musl-dev zlib1g-dev libjpeg-dev libmariadb3 libmariadb-dev libffi-dev



COPY . /usr/src/app/

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
