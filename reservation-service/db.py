import os
from dotenv import load_dotenv

try:
	from pymongo import MongoClient
except Exception:
	MongoClient = None

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

DB_NAME = os.getenv("DB_NAME")


DB_MODE = "memory"
reservation_collection = None
memory_reservations = {}

if MongoClient is not None:
	try:
		# Keep timeout low so service remains responsive when MongoDB is unavailable.
		client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=1500)
		client.admin.command("ping")
		db = client[DB_NAME]
		reservation_collection = db["reservations"]
		DB_MODE = "mongo"
	except Exception:
		DB_MODE = "memory"
		reservation_collection = None