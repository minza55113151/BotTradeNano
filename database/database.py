import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(os.getcwd())

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
    def log(json_data: dict):
        db["logs"].insert_one(json_data)