#!/bin/bash

# Wait for the postgres container to be ready before running the Django migrations
echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
sleep 5

python manage.py createsuperuser --no-input

echo "Creating Migrations..."
python manage.py makemigrations
echo ====================================

echo "Starting Migrations..."
python manage.py migrate
echo ====================================

echo "Starting Server..."
python manage.py runserver 0.0.0.0:8000