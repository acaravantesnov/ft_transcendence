#!/bin/bash

# I think it should be on Dockerfile, but it's not working there
service redis-server start

python3 manage.py createsuperuser --no-input

echo "Creating Migrations..."
python3 manage.py makemigrations
echo ====================================

echo "Starting Migrations..."
python3 manage.py migrate
echo ====================================

echo "Starting Server..."
python3 manage.py runserver 0.0.0.0:8000
