#!/bin/sh
build:
	docker image rm -f saturnphp/api.todayintel.com:latest && docker build -t saturnphp/api.todayintel.com:latest --no-cache --progress=plain . --build-arg CACHEBUST=$(date +%s)
dev:
	docker-compose -f docker-compose.yml up  --remove-orphans
down:
	docker-compose down
ssh:
	docker exec -it api.todayintel.com /bin/zsh
publish:
	docker push saturnphp/api.todayintel.com:latest
