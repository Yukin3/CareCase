import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

with open("data/scenario_scripts.json", "r", encoding="utf-8") as f:
    scenario_scripts = json.load(f)


client = MongoClient(MONGODB_URI)
db = client["CareCase"] 
collection = db["scenario_scripts"]

collection.delete_many({})
collection.insert_many(scenario_scripts)

print("Scripts uploaded!")
