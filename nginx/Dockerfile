FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf
COPY iwe-server.conf /etc/nginx/sites-available/

RUN mkdir -p /etc/nginx/sites-enabled/
RUN ln -s /etc/nginx/sites-available/iwe-server.conf /etc/nginx/sites-enabled/
