# Order System

## Простое веб-приложение для управления заказами. Позволяет создавать заказы, изменять их статус и отправлять уведомления по электронной почте.

### Технологии

**Backend**: Django (Python 3.12) + Django REST Framework  
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DjangoREST](https://img.shields.io/badge/Django%20REST-ff1709?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)

**База данных**: PostgreSQL  
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

**Очередь задач**: Celery + Redis  
[![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryproject.org/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)

**Веб-сервер**: Nginx + Gunicorn  
[![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)](https://gunicorn.org/)

**Контейнеризация**: Docker + Docker Compose  
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/)

**GitHub Actions**  
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)

## Запуск приложения

### Требования

- Установленный Docker и Docker Compose.

### Инструкция по запуску

## 1. Склонируйте репозиторий:

```bash
  git clone https://github.com/scorp5438/order_system.git
  cd order_system
``` 

## 2. Создайте файл .env в корне проекта и заполните его переменными окружения. Пример:

    DJANGO_SECRET_KEY=
 
    DJANGO_DEBUG=

    POSTGRES_NAME_DB=
    
    POSTGRES_USER_NAME=
    
    POSTGRES_PASSWORD=
    
    POSTGRES_HOST=
    
    POSTGRES_PORT=
    
    LOG_LEVEL_STREAM=
    
    LOG_LEVEL_FILE=
    
    REDIS_HOST=
    
    EMAIL_PASSWORD=

## 3. Запустите приложение с помощью Docker Compose:

```bash
  docker-compose up --build
```

# Руководство по запуску и использованию приложения

## 4. Запуск приложения

После запуска приложение будет доступно по следующим адресам:

- **API**: [http://localhost:80/api/](http://localhost:80/api/)
- **Админка**: [http://localhost:80/admin/](http://localhost:80/admin/)  

`* ВАЖНО Чтобы зайти в админку необходимо находясь в корне проекта создать superuser. Команда:`

```bash
  sudo docker ps
  sudo docker exec -it {id контейнера fastapi} /bin/bash
  python manage.py createsuperuser
```
`Далее задать логин и пароль например admin/1234`


## 5. Остановка приложения

Чтобы остановить приложение, выполните команду:
```bash 
  docker-compose down
```

## 6. API Endpoints

- **Создание заказа**:  
  `POST /api/v1/orders/`

- **Получение списка заказов**:  
  `GET /api/v1/orders/`

- **Изменение статуса заказа**:  
  `PATCH /api/v1/orders/<id>/`

- **Получение информации о заказе**:  
  `GET /api/v1/orders/<id>/`

## 7. Примеры запросов

### Создание заказа

```
POST /api/v1/orders/
{
    "product_name": "Laptop",
    "quantity": 1,
    "customer_email": "customer@example.com"
}
```

### Изменение статуса заказа

```
PATCH /api/v1/orders/1/
{
    "status": "processing"
}
```

### Получение списка заказов

```
GET /api/v1/orders/
```

### Получение информации о заказе

```
GET /api/v1/orders/<id>/
```

## 8. Фильтрация и пагинация

### Фильтрация
Заказы можно фильтровать по полям `status`, `product_name` и `customer_email`. Примеры:

- `GET /api/v1/orders/?status=completed`
- `GET /api/v1/orders/?product_name__icontains=laptop`
- `GET /api/v1/orders/?customer_email__icontains=example`

### Пагинация
Список заказов разбит на страницы. По умолчанию на одной странице отображается 10 заказов. Пример:

- `GET /api/v1/orders/?page=2`

## 9. Логирование
Логи приложения сохраняются в директории `logs/`. Логи Celery задач также записываются в файл.
