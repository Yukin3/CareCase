import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

with open("data/scenario_videos.json", "r", encoding="utf-8") as f:
    scenario_videos = json.load(f)


client = MongoClient(MONGODB_URI)
db = client["CareCase"] 
collection = db["scenario_videos"]

collection.delete_many({})
collection.insert_many(scenario_videos)

print("Vidoes uploaded!")
