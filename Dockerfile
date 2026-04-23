FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install django psycopg2-binary gunicorn
CMD python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8200 --timeout 120 --workers 4
