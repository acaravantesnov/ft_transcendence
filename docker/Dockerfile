FROM python:3.10-slim-bullseye

# install dependencies
RUN apt-get update
RUN apt-get install -y netcat redis-server vim net-tools

# Install app dependencies
COPY ./tools/requirements.txt .
RUN pip install -r requirements.txt

# Start redis
RUN chmod 777 /etc/redis/redis.conf
# RUN service redis-server start

# Set unbuffered output for python
ENV PYTHONUNBUFFERED 1

# Create app directory
WORKDIR /app

# Bundle app source
COPY ./srcs .
COPY ./tools .

RUN chmod +x ./django.sh

#RUN rm ./requirements.txt ./django.sh

# entrypoint to run the django.sh file with bash
ENTRYPOINT ["/bin/bash", "django.sh"]
