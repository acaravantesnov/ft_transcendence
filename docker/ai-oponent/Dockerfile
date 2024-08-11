# FROM python:3.10-slim-bullseye
FROM pytorch/pytorch

# install dependencies
RUN apt-get update
# RUN apt-get install -y ...

# Install app dependencies
COPY ./tools/requirements.txt .
RUN pip install -r requirements.txt

# Bundle app source
COPY ./srcs .
COPY ./tools .

# Make the django.sh file executable
RUN chmod +x ./main.py

# entrypoint to run the django.sh file with bash
ENTRYPOINT ["python", "main.py"]
# ENTRYPOINT ["tail", "-f", "/dev/null"]
