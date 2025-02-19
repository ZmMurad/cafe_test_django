# ☕ Cafe Orders Management System

Управление заказами в кафе с использованием Django + Docker + REST API

![Django](https://img.shields.io/badge/Django-4.2-green)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

## 🚀 Быстрый старт

### Требования
- Docker Engine ≥ 20.10
- Docker Compose ≥ 2.20

### Запуск проекта
```bash
# 1. Клонировать репозиторий
git clone https://github.com/ZmMurad/cafe_test_django

# 2. Настроить окружение
cp .env.example .env
# Отредактируйте .env при необходимости

# 3. Запустить контейнеры
docker-compose up -d --build

# 4. Применить миграции
docker-compose exec web python manage.py migrate

# 5 Запустить collectstatic
docker-compose exec web python manage.py collectstatic

# 6. Создать администратора (опционально)
docker-compose exec web python manage.py createsuperuser
```

## 🌐 Доступные адреса

| Сервис                | URL                          |
|-----------------------|------------------------------|
| Веб-интерфейс         | http://localhost:8000/orders |
| Админ-панель          | http://localhost:8000/admin  |
| API Documentation     | http://localhost:8000/swagger|
| REST API              | http://localhost:8000/api    |

## 🔧 Технологии

- **Backend**: 
  ![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django) 
  ![DRF](https://img.shields.io/badge/DRF-3.14-red?logo=django)
- **Database**: 
  ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
- **Infrastructure**: 
  ![Docker](https://img.shields.io/badge/Docker-24.0-2496ED?logo=docker) 
  ![Compose](https://img.shields.io/badge/Compose-2.20-384D54?logo=docker)
- **Auth**: 
  ![JWT](https://img.shields.io/badge/JWT-Optional-yellow?logo=jsonwebtokens)
- **Docs**: 
  ![Swagger](https://img.shields.io/badge/Swagger-3.0-85EA2D?logo=swagger)

## ⚙️ Конфигурация

Основные переменные окружения (`.env`):
```ini
DEBUG=0
SECRET_KEY=your-secret-key
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

##  📚 Документация API

Доступна через Swagger UI:

* Interactive Docs: http://localhost:8000/swagger
* Schema: http://localhost:8000/swagger.json

## 🛠 Команды управления

```
# Остановить контейнеры
docker-compose down

# Просмотр логов
docker-compose logs -f web

# Запуск тестов
docker-compose exec web python manage.py test

# Создание миграций
docker-compose exec web python manage.py makemigrations
```

