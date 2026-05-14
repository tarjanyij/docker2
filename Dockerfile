FROM python:3.11-slim

# Python optimalizálás
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# requirements előbb (cache miatt)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# projekt másolása
COPY . .

# static gyűjtés
RUN python manage.py collectstatic --noinput

# nem root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8200

CMD ["sh", "-c", "python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8200 --workers 4 --timeout 120"]
