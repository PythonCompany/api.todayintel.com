#!/bin/sh
# Makefile for v1 nlp api
build:
	docker build -t cornatul/nlp:v1 --progress=plain .
build-fresh:
	docker image rm -f cornatul/nlp:v1 && docker build -t cornatul/nlp:v1 --no-cache --progress=plain . --build-arg CACHEBUST=$(date +%s)
up:
	docker-compose up -d  --remove-orphans
up-dev:
	docker-compose -f docker-compose.yml up  --remove-orphans
stop:
	docker-compose down
ssh:
	docker exec -it nlp /bin/zsh
publish:
	docker push cornatul/nlp:v1
