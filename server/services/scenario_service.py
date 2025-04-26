from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)
db = client["CareCase"]
collection = db["scenarios"]

def get_all_scenarios():
    return list(collection.find({}, {"_id": 0}))

def get_scenario_by_id(scenario_id: str):
    return collection.find_one({"id": scenario_id}, {"_id": 0})
