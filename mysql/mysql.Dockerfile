FROM mysql:8

#COPY utf8.cnf /etc/mysql/conf.d/
COPY init_db.sql /docker-entrypoint-initdb.d/