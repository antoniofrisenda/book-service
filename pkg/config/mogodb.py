import os
from pymongo import MongoClient


client = MongoClient(os.getenv('MONGO_URL'))
db = client[os.getenv('MONGO_DB_NAME')]

def get_mongoDb():
    try:
        client.admin.command('ping')
        return db
    except Exception as e:
        print(f"✗ Errore: {e}")
        raise
