# Makefile

build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

logs:
	docker-compose logs

# Rebuild the images and restart the containers
rebuild:
	docker-compose down
	docker-compose up --build

# Start the containers in detached mode
up-detached:
	docker-compose up -d

# Stop the containers
stop:
	docker-compose stop

# Remove the containers
rm:
	docker-compose rm -f
