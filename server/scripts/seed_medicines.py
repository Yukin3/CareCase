import pandas as pd
import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client["CareCase"]
collection = db["medicines"]

# Load the medicine dataset CSV
csv_path = "data/datasets/medicine_dataset.csv"
df = pd.read_csv(csv_path)

# Normalize column names
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Clean and restructure data
structured_data = []
for _, row in df.iterrows():
    entry = {
        "name": str(row["name"]).strip(),
        "category": str(row["category"]).strip(),
        "dosage_form": str(row["dosage_form"]).strip(),
        "strength": str(row["strength"]).strip(),
        "manufacturer": str(row["manufacturer"]).strip(),
        "indication": str(row["indication"]).strip(),
        "classification": str(row["classification"]).strip().lower()
    }
    structured_data.append(entry)

# Avoid inserting duplicates by checking existing names
existing_names = set(doc["name"] for doc in collection.find({}, {"name": 1}))
new_entries = [entry for entry in structured_data if entry["name"] not in existing_names]

if new_entries:
    collection.insert_many(new_entries)
    print(f"✅ Inserted {len(new_entries)} new records into MongoDB.")
else:
    print("No new records to insert.")

# ✅ Export a lightweight JSON sample
export_path = "data/export/sample_medicines.json"
os.makedirs(os.path.dirname(export_path), exist_ok=True)

if new_entries:
    export_sample = new_entries[:30]
else:
    # fallback to pulling from Mongo if nothing new was added
    export_sample = list(collection.find({}, {"_id": 0}).limit(30))

with open(export_path, "w", encoding="utf-8") as f:
    json.dump(export_sample, f, indent=2)

print(f"✅ Exported sample medicines to {export_path}")
