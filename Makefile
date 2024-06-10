# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: acaravan <acaravan@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/13 17:01:21 by mortega-          #+#    #+#              #
#    Updated: 2024/06/10 15:19:54 by acaravan         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

docker_dir = ./docker
docker_file = docker-compose.yml
docker_yml = $(docker_dir)/$(docker_file)
docker_compose = docker compose
 
PORT = 8000
HOST = 0.0.0.0

all: up

build:
	$(docker_compose) -f $(docker_yml) build $(c)

start:
	$(docker_compose) -f $(docker_yml) start $(c)

stop:
	$(docker_compose) -f $(docker_yml) stop $(c)

restart: stop start

down:
	$(docker_compose) -f $(docker_yml) down $(c)

destroy:
	$(docker_compose) -f $(docker_yml) down -v $(c)

recreate: destroy up

ps:
	$(docker_compose) -f $(docker_yml) ps

login-db:
	$(docker_compose) -f $(docker_yml) exec db psql -d postgres -U postgres

login-prj:
	$(docker_compose) -f $(docker_yml) exec djangoapp /bin/bash

runserver:
	$(docker_compose) -f $(docker_yml) exec djangoapp python manage.py runserver $(HOST):$(PORT)

up:
	$(docker_compose) -f ./docker/docker-compose.yml up -d --build

