# Используем официальный образ PostgreSQL
FROM postgres:15

ENV POSTGRES_USER myuser
ENV POSTGRES_PASSWORD mypassword
ENV POSTGRES_DB mydatabase

EXPOSE 5432

# CMD ["postgres"]
