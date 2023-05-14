import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

load_dotenv()
MONGO_CONNECTION_URL = os.getenv("MONGO_CONNECTION_URL")

try:
    client = MongoClient(MONGO_CONNECTION_URL)
    db = client['nanobot']
except Exception as e:
    print(e)
    raise Exception("Cannot connect to MongoDB")

class DB:
    @staticmethod
    def get_customers():
        return list(db["customers"].find())

    @staticmethod
    def log_trade(json_data: dict):
        json_data["timestamp"] = datetime.now().isoformat()
        db["trade_logs"].insert_one(json_data)
        

if __name__ == "__main__":
    pass