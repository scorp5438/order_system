FROM python:3.12

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./order_system/ .
COPY fixtures_orders.json .

RUN python manage.py migrate
RUN python manage.py loaddata fixtures_orders.json

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "order_system.wsgi:application"]