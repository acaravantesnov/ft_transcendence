#!/bin/bash

# I think it should be on Dockerfile, but it's not working there
service redis-server start

python manage.py createsuperuser --no-input

echo "Creating Migrations..."
python manage.py makemigrations
echo ====================================

echo "Starting Migrations..."
python manage.py migrate
echo ====================================

echo "Starting Server..."
python manage.py runserver 0.0.0.0:8000
