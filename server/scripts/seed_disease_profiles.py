import pandas as pd
import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve MongoDB URI from the environment variable
MONGODB_URI = os.getenv("MONGODB_URI")

# Load CSV (update with your actual path)
csv_path = "data/datasets/Disease_symptom_and_patient_profile_dataset.csv"
df = pd.read_csv(csv_path)

# Normalize column names
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Map Yes/No to boolean
bool_map = {"yes": True, "no": False}

# Clean and restructure data
structured_data = []
for _, row in df.iterrows():
    entry = {
        "disease": str(row["disease"]).strip(),
        "symptoms": {
            "fever": bool_map.get(str(row["fever"]).strip().lower(), False),
            "cough": bool_map.get(str(row["cough"]).strip().lower(), False),
            "fatigue": bool_map.get(str(row["fatigue"]).strip().lower(), False),
            "difficulty_breathing": bool_map.get(str(row["difficulty_breathing"]).strip().lower(), False)
        },
        "patient_profile": {
            "age": int(row["age"]),
            "gender": str(row["gender"]).strip().lower(),
            "blood_pressure": str(row["blood_pressure"]).strip().lower(),
            "cholesterol_level": str(row["cholesterol_level"]).strip().lower()
        },
        "outcome": str(row["outcome_variable"]).strip().lower()
    }
    structured_data.append(entry)

# Insert into MongoDB (skip existing entries)
try:
    client = MongoClient(MONGODB_URI)
    db = client["CareCase"]
    collection = db["disease_profiles"]

    # Iterate over the structured_data and insert only non-existing entries
    inserted_count = 0
    for entry in structured_data:
        # Check if the disease already exists in the collection (based on the disease name)
        existing_entry = collection.find_one({"disease": entry["disease"]})
        if not existing_entry:
            # Insert only if no existing entry with the same disease
            collection.insert_one(entry)
            inserted_count += 1
    
    print(f"✅ Inserted {inserted_count} new records into MongoDB successfully.")
except Exception as e:
    print(f"❌ MongoDB insert failed: {e}")

# Prepare the export directory
export_dir = "data"
if not os.path.exists(export_dir):
    os.makedirs(export_dir)

# Export lightweight .json (e.g., first 30 entries)
json_path = os.path.join(export_dir, "sample_disease_profiles.json")
with open(json_path, "w", encoding="utf-8") as f:
    # Convert ObjectId to string before dumping to JSON
    for entry in structured_data[:30]:
        if "_id" in entry:
            entry["_id"] = str(entry["_id"])

    json.dump(structured_data[:30], f, indent=2)

print(f"✅ Exported sample diseases to {json_path}")
