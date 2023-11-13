#!/bin/sh
# Makefile for v1 nlp api
build:
	docker build -t cornatul/nlp:v1 --progress=plain .
build-fresh:
	docker build -t cornatul/nlp:v1 --no-cache --progress=plain .
up:
	docker-compose up -d
up-dev:
	docker-compose -f docker-compose-dev.yml up
stop:
	docker-compose down
