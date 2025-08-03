FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=desafio_iabs.settings

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

WORKDIR /app/desafio_iabs

RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

RUN python manage.py collectstatic --noinput

EXPOSE 8000

COPY --chown=appuser:appuser entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh
    
ENTRYPOINT ["/app/entrypoint.sh"]