ifneq (,$(wildcard ./.env))
	include .env
	export
endif

run-debug: 
	fastapi dev main.py

up: 
	docker-compose up -d

logs:
	docker logs mongodb

down:
	docker-compose down

