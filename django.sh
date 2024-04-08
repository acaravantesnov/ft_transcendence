#!/bin/bash

# Wait for the postgres container to be ready before running the Django migrations
echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
sleep 5

# Verificar si el superusuario ya existe
if python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(username='admin').exists())" | grep -q "True"; then
    echo "Superuser already exists"
else
    # Crear el superusuario
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password')" | python manage.py shell
    echo "Superuser created successfully (username: admin, password: password)"
fi

echo "Creating Migrations..."
python manage.py makemigrations TranscendenceApp
echo ====================================

echo "Starting Migrations..."
python manage.py migrate
echo ====================================

echo "Starting Server..."
python manage.py runserver 0.0.0.0:8000