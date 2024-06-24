FROM python:3.10-slim-bullseye

# install dependencies
RUN apt-get update
RUN apt-get install -y netcat redis-server vim net-tools

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

# Configure openssl (SSL - Secure Sockets Layer).
# - "req" with "-x509" generates a self-signed certificate.
# - "-nodes" indicates not to encrypt the private key with a password.
# - "-out" specifies where the certificate should be stored.
# - "-keyout" specifies where the private key should be stored.
# - "-subj" specifies the subject of the certificate.
RUN mkdir certs
RUN openssl req -x509 -days 365 -nodes -newkey rsa:4096 \
    -out ./certs/ft_transcendence.crt \
    -keyout ./certs/ft_transcendence.key \
    -subj "/C=ES/ST=Spain/L=Spain/O=42School/OU=acaravan/CN=acaravan/UID=login"

# Give user permissions to the certificates
RUN chmod +r ./certs/ft_transcendence.crt ./certs/ft_transcendence.key

# Make the django.sh file executable
RUN chmod +x ./django.sh

#RUN rm ./requirements.txt ./django.sh

# entrypoint to run the django.sh file with bash
ENTRYPOINT ["/bin/bash", "django.sh"]
