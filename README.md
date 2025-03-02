# Order System

## Простое веб-приложение для управления заказами. Позволяет создавать заказы, изменять их статус и отправлять уведомления по электронной почте.

### Технологии

- **Backend**: Django, Django REST Framework (DRF)
- **Database**: PostgreSQL
- **Task Queue**: Celery + Redis
- **Web Server**: Nginx
- **Containerization**: Docker + Docker Compose

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

    SECRET_KEY=
 
    DEBUG=

    POSTGRES_NAME_DB=
    
    POSTGRES_USER_NAME=
    
    POSTGRES_PASSWORD=
    
    POSTGRES_HOST=
    
    POSTGRES_PORT=
    
    LOG_LEVEL_STREAM=
    
    LOG_LEVEL_FILE=
    
    REDIS_HOST=
    
    EMAIL_PASSWORD

## 3. Запустите приложение с помощью Docker Compose:

```bash
  docker-compose up --build
```

# Руководство по запуску и использованию приложения

## 4. Запуск приложения

После запуска приложение будет доступно по следующим адресам:

- **API**: [http://localhost:8000/api/](http://localhost:8000/api/)
- **Админка**: [http://localhost:8000/admin/](http://localhost:8000/admin/)  
  **Логин/пароль**: `admin/admin`

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
GET /api/v1/orders/
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

## 9. Тестирование

### Запуск тестов
Чтобы запустить тесты, выполните команду:

```bash
  docker-compose run web python manage.py test
```
### Запуск тестов Celery
Для тестирования задач Celery используйте команду:

```bash
  docker-compose run web pytest
```

## 10. Логирование
Логи приложения сохраняются в директории `logs/`. Логи Celery задач также записываются в файл.