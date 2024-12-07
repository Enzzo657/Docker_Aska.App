# Используем официальный образ PostgreSQL 16
FROM postgres:16

# Установка переменных окружения для первичной инициализации
ENV POSTGRES_USER=enzzo
ENV POSTGRES_PASSWORD=123456
ENV POSTGRES_DB=mybase

# Копируем конфиги
COPY configs/postgresql.conf /etc/postgresql/postgresql.conf
COPY configs/pg_hba.conf /etc/postgresql/pg_hba.conf

# Применяем пользовательские конфиги
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
