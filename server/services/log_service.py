from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)
db = client["CareCase"]
collection = db["interaction_logs"]

def save_interaction_log(log_data):
    try:
        result = collection.insert_one(log_data)
        return str(result.inserted_id)
    except Exception as e:
        print("❌ MongoDB insert failed:", e)
        return None
