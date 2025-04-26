import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")


with open("data/voice_profiles.json", "r", encoding="utf-8") as f:
    voice_profiles = json.load(f)


client = MongoClient(MONGODB_URI)
db = client["CareCase"] 
collection = db["voice_profiles"]

collection.delete_many({})
collection.insert_many(voice_profiles)

print("Voice profiles uploaded!")
