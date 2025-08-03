#!/bin/bash

echo "Starting Django application..."

cd /app/desafio_iabs

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin / admin123')
else:
    print('Superuser already exists')
" 2>/dev/null || echo "Superuser creation skipped"

echo "Starting Django server on 0.0.0.0:8000"
exec python manage.py runserver 0.0.0.0:8000