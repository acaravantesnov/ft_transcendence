#!/bin/bash
set -e

service redis-server start

until nc -z -v -w30 db 5432
do
  echo "Waiting for PostgreSQL to start..."
  sleep 5
done

echo "Creating Migrations..."
python3 manage.py makemigrations
python3 manage.py makemigrations TranscendenceApp
echo ====================================

echo "Starting Migrations..."
python3 manage.py migrate
echo ====================================

# Create superuser giving username and password to the prompt

if [ $(echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME}', '${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}')" | python3 manage.py shell) ]
then
	echo ":)"
fi

echo "Starting Server..."
python3 manage.py runserver 0.0.0.0:8000
