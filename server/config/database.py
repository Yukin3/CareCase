import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)
db = client["CareCase"]

# Collections
scenarios_collection = db["scenarios"]
scripts_collection = db["scenario_scripts"]
videos_collection = db["scenario_videos"]
