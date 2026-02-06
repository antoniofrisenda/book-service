from dataclasses import dataclass
import os
from pymongo import MongoClient
from pymongo.database import Database

@dataclass
class MongoConnection:
    client: MongoClient
    database: Database
    

def get_mongoDb(
    mongo_url=os.getenv('MONGO_URL'),
    db_name=os.getenv("MONGO_DB_NAME")) -> MongoConnection:
    
    client = MongoClient(mongo_url)
    client.admin.command("ping")
    return MongoConnection(client=client, database=client[db_name])
