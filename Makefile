#!/bin/sh
build:
	docker image rm -f cornatul/api.todayintel.com:v1 && docker build -t cornatul/api.todayintel.com:v1 --no-cache --progress=plain . --build-arg CACHEBUST=$(date +%s)
prod:
	docker-compose -f docker-compose-prod.yml up
dev:
	docker-compose -f docker-compose.yml up  --remove-orphans
stop:
	docker-compose down
ssh:
	docker exec -it api.todayintel.com /bin/zsh
publish:
	docker push cornatul/api.todayintel.com:v1
