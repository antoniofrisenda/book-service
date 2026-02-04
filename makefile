export MONGO_DB_NAME= test-db
export MONGO_URL= mongodb://root:pass@localhost:27017/test-db?authSource=admin&retryWrites=true&w=majority

run-debug: 
	fastapi dev main.py

up: 
	docker-compose up -d

logs:
	docker logs mongodb

down:
	docker-compose down

