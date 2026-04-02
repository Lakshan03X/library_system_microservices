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
member_collection = None
memory_members = {}
connection_error = None

if MongoClient is not None:
    try:
        # Keep timeout low so service remains responsive when MongoDB is unavailable.
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        db = client[DB_NAME]
        member_collection = db["members"]
        DB_MODE = "mongo"
        print(f"[Member Service] Connected to MongoDB: {DB_NAME}")
    except Exception as e:
        DB_MODE = "memory"
        member_collection = None
        connection_error = str(e)
        print(f"[Member Service] MongoDB connection failed: {e}")
        print("[Member Service] Using in-memory storage (data will be lost on restart)")
else:
    print("[Member Service] pymongo not installed, using in-memory storage")
