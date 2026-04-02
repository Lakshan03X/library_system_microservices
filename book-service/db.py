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
book_collection = None
memory_books = {}
connection_error = None

if MongoClient is not None:
    try:
        # Keep timeout low so service remains responsive when MongoDB is unavailable.
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        db = client[DB_NAME]
        book_collection = db["books"]
        DB_MODE = "mongo"
        print(f"[Book Service] Connected to MongoDB: {DB_NAME}")
    except Exception as e:
        DB_MODE = "memory"
        book_collection = None
        connection_error = str(e)
        print(f"[Book Service] MongoDB connection failed: {e}")
        print("[Book Service] Using in-memory storage (data will be lost on restart)")
else:
    print("[Book Service] pymongo not installed, using in-memory storage")