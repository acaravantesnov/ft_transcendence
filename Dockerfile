FROM python:3.11-slim-bullseye

# install dependencies
RUN apt-get update && apt-get install -y netcat


# Set unbuffered output for python
ENV PYTHONUNBUFFERED 1

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Bundle app source
COPY . .

RUN chmod +x /app/django.sh

# entrypoint to run the django.sh file
ENTRYPOINT ["/app/django.sh"]