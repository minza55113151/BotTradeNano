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
    customers = []
    @staticmethod
    def get_customers(refetch=False):
        if len(DB.customers) <= 0 or refetch:
            DB.customers.clear()
            DB.customers += list(db["customers"].find())
        return DB.customers

    @staticmethod
    def log_trade(json_data: dict):
        json_data["timestamp"] = datetime.utcnow().isoformat()
        db["trade_logs"].insert_one(json_data)
    
    @staticmethod
    def log_alert(json_data: dict):
        json_data["timestamp"] = datetime.utcnow().isoformat()
        db["alert_logs"].insert_one(json_data)


if __name__ == "__main__":
    pass