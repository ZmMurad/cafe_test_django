# Используем официальный python образ
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем список зависимостей
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем код проекта
COPY . /app/

# Открываем порт
EXPOSE 8000

# Запускаем команду по умолчанию
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
