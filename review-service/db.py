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
review_collection = None
memory_reviews = {}
connection_error = None

if MongoClient is not None:
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        db = client[DB_NAME]
        review_collection = db["reviews"]
        DB_MODE = "mongo"
        print(f"[Review Service] Connected to MongoDB: {DB_NAME}")
    except Exception as e:
        DB_MODE = "memory"
        review_collection = None
        connection_error = str(e)
        print(f"[Review Service] MongoDB connection failed: {e}")
        print("[Review Service] Using in-memory storage (data will be lost on restart)")
else:
    print("[Review Service] pymongo not installed, using in-memory storage")