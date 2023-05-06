import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_CONNECTION_URL = os.getenv("MONGO_CONNECTION_URL")

try:
    client = MongoClient(MONGO_CONNECTION_URL)
    db = client['nanobot']
except Exception as e:
    print(e)
    raise Exception("Cannot connect to MongoDB")