FROM nginx

COPY ./conf/nginx.conf /etc/nginx/nginx.conf

RUN apt-get update && apt-get install -y vim openssl

# Generate SSL certificate
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/ft_transcendence.key \
    -out /etc/ssl/certs/ft_transcendence.crt \
    -subj "/C=ES/ST=Spain/L=Spain/O=42School/OU=acaravan/CN=acaravan/UID=login"