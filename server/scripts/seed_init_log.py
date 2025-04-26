import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

with open("data/scenario_stomach_pain_rice_001_c2bdd3.json", "r", encoding="utf-8") as f:
    interaction_log = json.load(f)

interaction_logs = [interaction_log]

client = MongoClient(MONGODB_URI)
db = client["CareCase"] 
collection = db["interaction_logs"]

collection.delete_many({})
collection.insert_many(interaction_logs)

print("Log uploaded!")
