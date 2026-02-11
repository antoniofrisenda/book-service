export MONGO_DB_NAME= book-service
export MONGO_URI= mongodb://root:pass@localhost:27017/book-service?authSource=admin&retryWrites=true&w=majority

run-debug: 
	fastapi dev main.py

up: 
	docker-compose up -d

down:
	docker-compose down

