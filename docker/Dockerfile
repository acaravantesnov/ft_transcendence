FROM python:3.11-slim-bullseye

# install dependencies
RUN apt-get update && apt-get install -y netcat


# Set unbuffered output for python
ENV PYTHONUNBUFFERED 1

# Install app dependencies
COPY ./tools/requirements.txt .
RUN pip install -r requirements.txt

COPY ./tools/django.sh .
RUN chmod +x ./django.sh

# Create app directory
WORKDIR /app

# Bundle app source
COPY ./srcs/. .

#RUN rm ./requirements.txt ./django.sh

# entrypoint to run the django.sh file
ENTRYPOINT ["/django.sh"]
