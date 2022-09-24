# pull official base image
FROM python:3.8
# python:3.8.0-alpine

# set work directory
#WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST "redis"
#ENV http_proxy http://192.168.1.12:3128
#ENV https_proxy http://192.168.1.12:3128

#RUN apt-get update
RUN apt-get install -y bash libjpeg-dev libmariadb3 libmariadb-dev

COPY . /usr/src/app/
# set work directory
WORKDIR /usr/src/app

# install dependencies
#RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -U 'Twisted[tls,http2]'
RUN python3 manage.py makemigrations && python3 manage.py migrate

#WORKDIR /usr/src/letsencrypt/
#RUN test -f live/iwe-server.shop/fullchain.pem && echo "exists"
#RUN cp live/iwe-server.shop/fullchain.pem /usr/src/app/
#RUN test -f live/iwe-server.shop/privkey.pem && echo "exists"
#RUN cp live/iwe-server.shop/privkey.pem /usr/src/app/

#WORKDIR /usr/src/app

#RUN test -f fullchain.pem && echo "exists" || echo "x exist"
#RUN test -f privkey.pem && echo "exists" || echo "x exist"

#RUN gunicorn web_editor.wsgi:application --bind 0.0.0.0:8000 --daemon

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "web_editor.asgi:application"]