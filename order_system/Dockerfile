FROM python:3.12

RUN useradd -m alex

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

RUN pip cache purge

COPY . .

RUN chown -R alex:alex /app

USER alex

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "order_system.order_system.wsgi:application"]