import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

with open("data/scenarios.json", "r", encoding="utf-8") as f:
    scenarios = json.load(f)


client = MongoClient(MONGODB_URI)
db = client["CareCase"] 
collection = db["scenarios"]

collection.delete_many({})
collection.insert_many(scenarios)

print("Scenarios uploaded!")
