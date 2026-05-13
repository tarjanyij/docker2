FROM python:3.11
# 🔧 alap beállítások
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 👤 security (nem root user)
RUN useradd -m appuser
USER appuser

CMD python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8200 --timeout 120 --workers 4
