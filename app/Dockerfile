# Базовый образ
FROM python:3.10-slim

# Устанавливаем зависимости для работы Python (например, для psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение
COPY . .

# Указываем переменные окружения для Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Запуск приложения
CMD ["python", "app.py"]
