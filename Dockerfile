FROM python:3.8-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app

RUN set -ex \
        && apt-get update \
        && apt-get install -y --no-install-recommends \
                build-essential \
                libjpeg-dev \
                libmariadb3 \
                libmariadb-dev \
                nginx \
                supervisor \
        && rm -rf /var/lib/apt/lists/* \
        && echo "\ndaemon off;" >> /etc/nginx/nginx.conf \
        && rm /etc/nginx/sites-enabled/default \
        && chown -R www-data:www-data /var/lib/nginx \
        && sed -i -e 's#access_log /var/log/nginx/access.log;#access_log off;#' /etc/nginx/nginx.conf \
        && ln -sf /app/nginx-app.conf /etc/nginx/sites-enabled/ \
        && ln -sf /app/supervisor-app.conf /etc/supervisor/conf.d/ \
        && python -m venv /venv \
        && bash -c ": \
        && source /venv/bin/activate \
        && set -ex \
        && pip install -U 'Twisted[tls,http2]' \
        && pip install -r requirements.txt"

ENTRYPOINT ["bash", "-c", "source /venv/bin/activate && supervisord -n"]
