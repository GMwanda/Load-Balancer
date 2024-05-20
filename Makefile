# Makefile

build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

logs:
	docker-compose logs

rebuild:
	docker-compose down
	docker-compose up --build

up-detached:
	docker-compose up -d

stop:
	docker-compose stop

rm:
	docker-compose rm -f
