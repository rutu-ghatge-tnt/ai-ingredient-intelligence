# app/db/sync_mongodb.py  (sync for training scripts)
from pymongo import MongoClient
from app.config import MONGO_URI, DB_NAME

sync_client = MongoClient(MONGO_URI)
sync_db = sync_client[DB_NAME]
