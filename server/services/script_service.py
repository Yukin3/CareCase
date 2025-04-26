from pymongo import MongoClient
import os
import json
from dotenv import load_dotenv
from config.database import scripts_collection  

load_dotenv()

def format_script_lines(script_obj):
    formatted = {}
    for i, line in enumerate(script_obj.get("script", [])):
        formatted[f"line_{i}"] = line
    script_obj["script"] = formatted
    return script_obj

def get_all_scripts():
    return list(scripts_collection.find({}, {"_id": 0}))

def get_script_by_id(script_id: str):
    script = scripts_collection.find_one({"id": script_id}, {"_id": 0})
    return format_script_lines(script) if script else None

def get_scripts_for_scenario(scenario_id: str):
    return list(scripts_collection.find({"scenario_id": scenario_id}, {"_id": 0}))
