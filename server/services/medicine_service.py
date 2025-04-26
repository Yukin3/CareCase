from pymongo import MongoClient
import os
from dotenv import load_dotenv
from bson import ObjectId  # ✅ import this

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["CareCase"]
med_collection = db["medicines"]

def clean_doc(doc):
    doc["_id"] = str(doc["_id"])  # 👈 convert ObjectId to string
    return doc

def get_all_medicines(name=None, category=None, limit=20, skip=0):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if category:
        query["category"] = {"$regex": category, "$options": "i"}
    
    cursor = med_collection.find(query).skip(skip).limit(limit)
    return [clean_doc(doc) for doc in cursor]

def get_medicine_by_id(id):
    doc = med_collection.find_one({"_id": ObjectId(id)})
    return clean_doc(doc) if doc else None
