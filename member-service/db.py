from pymongo import MongoClient
from urllib.parse import quote_plus

username = "chamika"
password = quote_plus("chamika@1221")

MONGO_URL = f"mongodb+srv://{username}:{password}@cluster0.hkwxpze.mongodb.net/?appName=Cluster0&tls=true&tlsInsecure=true"

client = MongoClient(MONGO_URL)

db = client["library_management"]
members_collection = db["members"]