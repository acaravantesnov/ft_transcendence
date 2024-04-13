# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mortega- <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/13 17:01:21 by mortega-          #+#    #+#              #
#    Updated: 2024/04/13 18:38:34 by mortega-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

all: up

build:
	docker-compose -f ./docker-compose.yml build $(c)

up:
	docker-compose -f ./docker-compose.yml up -d --build

start:
	docker-compose -f ./docker-compose.yml start $(c)

stop:
	docker-compose -f ./docker-compose.yml stop $(c)

restart: stop start

down:
	docker-compose -f ./docker-compose.yml down $(c)

destroy:
	docker-compose -f ./docker-compose.yml down -v $(c)

recreate: destroy up

ps:
	docker-compose -f ./docker-compose.yml ps

login-db:
	docker-compose -f ./docker-compose.yml exec db /bin/bash

login-prj:
	docker-compose -f ./docker-compose.yml exec djangoapp /bin/bash
