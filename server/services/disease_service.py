from pymongo import MongoClient
import os
from dotenv import load_dotenv
import random

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client["CareCase"]
collection = db["disease_profiles"]

def get_unique_diseases():
    diseases = collection.distinct("disease")
    return diseases

def get_random_profile_for_disease(disease_name):
    profiles = list(collection.find({"disease": disease_name}))
    if not profiles:
        return None
    return random.choice(profiles)
