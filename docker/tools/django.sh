#!/bin/bash

service redis-server start

echo "Creating Migrations..."
python3 manage.py makemigrations
python3 manage.py makemigrations TranscendenceApp
echo ====================================

echo "Starting Migrations..."
python3 manage.py migrate
echo ====================================

# Create superuser giving username and password to the prompt
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME}', '${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}')" | python3 manage.py shell

echo "Starting Server..."
python3 manage.py runserver 0.0.0.0:8000
