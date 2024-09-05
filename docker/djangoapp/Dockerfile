FROM python:3.10-slim-bullseye

# install dependencies
RUN apt-get update
RUN apt-get install -y netcat redis-server vim net-tools
RUN apt-get install -y gettext

# Install app dependencies
COPY ./tools/requirements.txt .
RUN pip install -r requirements.txt

# Start redis
RUN chmod 777 /etc/redis/redis.conf

# Set unbuffered output for python
ENV PYTHONUNBUFFERED 1

# Create app directory
WORKDIR /app

# Bundle app source
COPY ./srcs .
COPY ./tools .

# Make the django.sh file executable
RUN chmod +x ./django.sh

# entrypoint to run the django.sh file with bash
ENTRYPOINT ["/bin/bash", "django.sh"]
